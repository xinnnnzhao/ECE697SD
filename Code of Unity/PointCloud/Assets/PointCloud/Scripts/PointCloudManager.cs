using UnityEngine;
using System.Collections;
using System.IO;
using System.Collections.Generic;

public class PointCloudManager : MonoBehaviour {

	public enum FileType
    {
		OFF,
		xyz,
		xyzrgb
    }

	// File
	public string dataPath;
	public FileType fileType;
	[Header("初始化")]
	public Color XyzInitColor;
	private string filename;
	public Material matVertex;

	// GUI
	private float progress = 0;
	private string guiText;
	private bool loaded = false;

	// PointCloud
	private GameObject pointCloud;

	public float scale = 1;
	public bool invertYZ = false;
	public bool forceReload = false;

	public int numPoints;
	public int numPointGroups;
	private int limitPoints = 65000;

	//private Vector3[] points;
	private List<Vector3> points;
	private List<Color> colors=new List<Color>();
	private Vector3 minValue;

	public float ReadInterval;
	private float m_Timer;

	GameObject pointGroup;

	public bool OnlyReadOnce;


	void Start () {
		m_Timer = ReadInterval;

		// Create Resources folder
		createFolders ();

		// Get Filename
		filename = Path.GetFileName(dataPath);

		loadScene ();
	}

    private void Update()
    {
		if(!OnlyReadOnce)
        {

			if(m_Timer>0)
			{
				m_Timer -= Time.deltaTime;
			}
			else
			{
				loadScene();
				Debug.Log("ReRead");
				m_Timer = ReadInterval;
			}
        }
	}



    void loadScene(){
		loadPointCloud();

		//// Check if the PointCloud was loaded previously
		//if (!Directory.Exists (Application.dataPath + "/Resources/PointCloudMeshes/" + filename)){
		//	UnityEditor.AssetDatabase.CreateFolder ("Assets/Resources/PointCloudMeshes", filename);
		//	loadPointCloud ();
		//} else if (forceReload){
		//	UnityEditor.FileUtil.DeleteFileOrDirectory(Application.dataPath + "/Resources/PointCloudMeshes/" + filename);
		//	UnityEditor.AssetDatabase.Refresh();
		//	UnityEditor.AssetDatabase.CreateFolder ("Assets/Resources/PointCloudMeshes", filename);
		//	loadPointCloud ();
		//} else
		//	// Load stored PointCloud
		//	loadStoredMeshes();
	}
	
	
	void loadPointCloud(){

        switch (fileType)
        {
            case FileType.OFF:
                {
					if (File.Exists(dataPath + ".off"))
					{
						// load off
						StartCoroutine("loadOFF", dataPath + ".off");
					}
					else
					{
						Debug.LogError("文件路径有误,或文件不存在");
					}
					break;
                }
            case FileType.xyz:
                {
					if (File.Exists(dataPath + ".xyz"))
					{
						StartCoroutine("loadOFF", dataPath + ".xyz");
					}
					else
					{
						Debug.LogError("文件路径有误,或文件不存在");
					}
					break;
				}
            case FileType.xyzrgb:
                {
					if (File.Exists(dataPath + ".xyzrgb"))
					{
						StartCoroutine("loadOFF", dataPath + ".xyzrgb");
					}
					else
					{
						Debug.LogError("文件路径有误,或文件不存在");
					}
					break;
                }
            default:
                break;
        }


	}
	
	// Load stored PointCloud
	void loadStoredMeshes(){

		Debug.Log ("Using previously loaded PointCloud: " + filename);

		GameObject pointGroup = Instantiate(Resources.Load ("PointCloudMeshes/" + filename)) as GameObject;

		loaded = true;
	}
	
	// Start Coroutine of reading the points from the OFF file and creating the meshes
	IEnumerator loadOFF(string dPath){

		// Read file
		FileStream fs = File.Open(dPath, FileMode.Open);
		StreamReader sr = new StreamReader(fs);
		//string[] buffer = sr.ReadLine ().Split(); // nPoints, nFaces
		string[] buffer; // nPoints, nFaces
		//numPoints = int.Parse (buffer[0]);
		//points = new Vector3[numPoints];
		points=new List<Vector3>();
		minValue = new Vector3();

		for (int i = 0;; i++)
		{
			string line = sr.ReadLine();
			if(line==null)
            {
				numPoints = i;
				break;
            }

			buffer = line.Split();

			if (!invertYZ)
				//points[i] = new Vector3 (float.Parse (buffer[0])*scale, float.Parse (buffer[1])*scale,float.Parse (buffer[2])*scale) ;
				points.Add(new Vector3(float.Parse(buffer[0]) * scale, float.Parse(buffer[1]) * scale, float.Parse(buffer[2]) * scale));
			else
				//points[i] = new Vector3(float.Parse(buffer[0]) * scale, float.Parse(buffer[2]) * scale, float.Parse(buffer[1]) * scale);
				points.Add(new Vector3(float.Parse(buffer[0]) * scale, float.Parse(buffer[2]) * scale, float.Parse(buffer[1]) * scale));

			if (buffer.Length >= 5)
				//colors[i] = new Color(int.Parse(buffer[3]) / 255.0f, int.Parse(buffer[4]) / 255.0f, int.Parse(buffer[5]) / 255.0f);
				colors.Add(new Color(float.Parse(buffer[3]), float.Parse(buffer[4]), float.Parse(buffer[5])));
			//else
			//	colors[i] = Color.cyan;

            // Relocate Points near the origin
            //calculateMin(points[i]);

            // GUI
            //progress = i *1.0f/(numPoints-1)*1.0f;
            //if (i%Mathf.FloorToInt(numPoints/20) == 0){
            //	guiText=i.ToString() + " out of " + numPoints.ToString() + " loaded";
            //	yield return null;
            //}
        }

  //      for (int i = 0; i < colors.Length; i++)
  //      {
		//	colors[i] = Color.cyan;
		//}

		
		// Instantiate Point Groups
		numPointGroups = Mathf.CeilToInt (numPoints*1.0f / limitPoints*1.0f);

		if (pointCloud != null)
		{
			Destroy(pointCloud);
			pointCloud = null;
		}
		pointCloud = new GameObject(filename);

		for (int i = 0; i < numPointGroups-1; i ++) {
			InstantiateMesh (i, limitPoints);
			if (i%10==0){
				guiText = i.ToString() + " out of " + numPointGroups.ToString() + " PointGroups loaded";
				yield return null;
			}
		}
		InstantiateMesh (numPointGroups-1, numPoints- (numPointGroups-1) * limitPoints);

		//Store PointCloud
		//UnityEditor.PrefabUtility.CreatePrefab ("Assets/Resources/PointCloudMeshes/" + filename + ".prefab", pointCloud);

		loaded = true;

		fs.Close();
	}

	
	void InstantiateMesh(int meshInd, int nPoints){
		// Create Mesh
		GameObject pointGroup = new GameObject(filename + meshInd);
		pointGroup.AddComponent<MeshFilter> ();
		pointGroup.AddComponent<MeshRenderer>().material = matVertex;
		//pointGroup.renderer.material = matVertex;

		pointGroup.GetComponent<MeshFilter> ().mesh = CreateMesh (meshInd, nPoints, limitPoints);
		pointGroup.transform.parent = pointCloud.transform;


		// Store Mesh
		//UnityEditor.AssetDatabase.CreateAsset(pointGroup.GetComponent<MeshFilter> ().mesh, "Assets/Resources/PointCloudMeshes/" + filename + @"/" + filename + meshInd + ".asset");
		//UnityEditor.AssetDatabase.SaveAssets ();
		//UnityEditor.AssetDatabase.Refresh();
	}

	Mesh CreateMesh(int id, int nPoints, int limitPoints){
		
		Mesh mesh = new Mesh ();
		
		Vector3[] myPoints = new Vector3[nPoints]; 
		int[] indecies = new int[nPoints];
		Color[] myColors = new Color[nPoints];

		for(int i=0;i<nPoints;++i) {
			myPoints[i] = points[id*limitPoints + i] - minValue;
			indecies[i] = i;
            switch (fileType)
            {
                case FileType.OFF:
                    break;
                case FileType.xyz:
                    {
						myColors[i] = XyzInitColor;
						break;
                    }
                case FileType.xyzrgb:
                    {
						myColors[i] = colors[id * limitPoints + i];
						break;
                    }
                default:
                    break;
            }

		}


		mesh.vertices = myPoints;
		mesh.colors = myColors;
		mesh.SetIndices(indecies, MeshTopology.Points,0);
		mesh.uv = new Vector2[nPoints];
		mesh.normals = new Vector3[nPoints];


		return mesh;
	}

	void calculateMin(Vector3 point){
		if (minValue.magnitude == 0)
			minValue = point;


		if (point.x < minValue.x)
			minValue.x = point.x;
		if (point.y < minValue.y)
			minValue.y = point.y;
		if (point.z < minValue.z)
			minValue.z = point.z;
	}

	void createFolders(){
		if(!Directory.Exists (Application.dataPath + "/Resources/"))
			UnityEditor.AssetDatabase.CreateFolder ("Assets", "Resources");

		if (!Directory.Exists (Application.dataPath + "/Resources/PointCloudMeshes/"))
			UnityEditor.AssetDatabase.CreateFolder ("Assets/Resources", "PointCloudMeshes");
	}


	void OnGUI(){


		if (!loaded){
			GUI.BeginGroup (new Rect(Screen.width/2-100, Screen.height/2, 400.0f, 20));
			GUI.Box (new Rect (0, 0, 200.0f, 20.0f), guiText);
			GUI.Box (new Rect (0, 0, progress*200.0f, 20), "");
			GUI.EndGroup ();
		}
	}

}
