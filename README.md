# ECE697SD

Project Proposal Overleaf Link: https://www.overleaf.com/9956381517dgvrjtymdnss

1. Point clouds

1.1 Point cloud stitching (alignment)
  
  Export point clouds from depth cameras using the Python third-party library Open3d and perform stitching (alignment)
  RealSense ( librealsenseSDK v2) is integrated into Open3D (v0.12+) and you can use it via C++ and Python APIs without the need for librealsense to install separate SDKs on Linux, macOS and Windows. Intel GitHub Link. https://github.com/IntelRealSense/librealsense/tree/master/wrappers/open3d
  Open3D is an open source library that supports rapid development of software for processing 3D data. open3D backend is implemented in C++ and exposed through a front-end interface in Python. open3D provides three data structures: point cloud, mesh, and RGB-D images. For each representation, open3D implements a set of basic processing algorithms, such as I/O, sampling, visualization and data conversion. In addition, some common algorithms are included, such as ICP alignment, which is the algorithm that implements point cloud stitching. open3d link: http://www.open3d.org/docs/latest/tutorial/sensor/index.html

1.2 Point cloud export.
  Currently it seems that the deep camera local visualization uses video frames, which are not yet clear.

1.3 Point cloud resolution reduction/downsampling.
  realsense camera: pyrealsense2.decimation_filter()
  open3d: Voxel downsampling

1.4 Point cloud compression (powershell script compressed and transferred)
  
  The following content is for extended learning only and is not implemented in this project.
  Point cloud compression status and development trend https://blog.csdn.net/baidu_35231778/article/details/116046090
  Google Draco: https://github.com/google/draco
  DracoUnity: https://github.com/atteneder/DracoUnity
  Draco is a library for compressing and decompressing 3D geometric meshes and point clouds. It is designed to improve the storage and transfer of 3D graphics. draco is designed and built for compression efficiency and speed. The code supports compression of points, connection information, texture coordinates, color information, normals, and any other general properties related to geometry. Using Draco, applications that use 3D graphics can be significantly reduced in size without compromising visual fidelity. For users, this means that applications can now be downloaded faster, 3D graphics can now be loaded faster in the browser, and VR and AR scenes can now be transferred and rendered quickly with a fraction of the bandwidth.Draco is distributed as C++ source code for compressing 3D graphics as well as C++ and Javascript decoders for encoding data.
  ! [))QXSHG_X @{$N)Q5}{BENF](https://user-images.githubusercontent.com/35893137/141601448-2afe24d1-2e2a-4bb8-b192-045e106da407.png)
  ! [L@Z U }_{VVL0J TPD@8WR](https://user-images.githubusercontent.com/35893137/141601645-3de36fff-7c19-4b37-bb42-f2b424f65364.png)

  Several good libraries (tools) for model optimization :
  ● https://github.com/zeux/meshoptimizer 3-D model optimization library
  ● https://github.com/zeux/meshoptimizer/tree/master/gltf A mesh optimization program implemented on top of meshoptimizer, which can directly optimize gltf models
  ● github.com/google/draco Google-developed mesh compression library, with very high compression rate
  ● github.com/CesiumGS/glt... Cesium developed gltf tool, can directly call Draco to compress gltf

2. Remote transfer

  AWS server, powershell call script


3. Unity reads point cloud files
  
  Unity can customize the frame refresh read xyz format file to achieve real-time reading, but can not read the depth of the camera in the point cloud file  
**Download point cloud file (client):**  
  First download the powershell script dowload.scp.ps1, and the path to be placed is to receive the point cloud
  Download path.
  Then use Powershell to start the script (./dowload.scp.ps1 out)  
 **Unity reads the point cloud:**  
  Use Unity to open the PointCloud project, and note that the Unity read path should be the location of the point cloud file.

4. Unity import VR devices
  
  HTC VIVE, VR Steram and Unity interaction


**Bottlenecks and challenges.**  
  
  1. To achieve character tracking, you need to separate the character and the scene point cloud, we can only do the character as an environmental element to achieve observation, by constantly refreshing the read point cloud file to achieve observation of the character's position.
  
  2. Unity real-time reading point cloud file
  
  3. Deep camera export point cloud file in real time
  
  4. Point cloud file in real-time transfer between computer A and computer B  
  

**PS**  
If we want to achieve real-time tracking of character point cloud, environment point cloud and character point cloud need to be separated first, and also need to process the character point cloud algorithmically, which is a huge challenge.  
Although RA provides some references, it seems that they are only relevant and do not solve the problem at the moment. Maybe we have to spend more time to explore.


**Responsibilities**  

Xiaohao Xia: Develop a project time plan, and communicate with the professor. Import the point cloud file into Unity and implement modeling in Unity at the Import the point cloud file into Unity and implement modeling in Unity at the same time.  

Yinxuan Wu: Responsible for the data capture of the depth camera, Point cloud stitching, read the point cloud file. save hardware, etc.  

Xintao Ding: Responsible for completing the remote transmission of the cloud file with Xin Zhao, preparing the project display, and project record, Importing model data into VR headset.  

Xin Zhao: Responsible for developing a software to complete remote transmission of cloud file, and second inspection experiment report.  

**Xia Xiaohao**  
**Completed**  
Select the appropriate point cloud reading plug-in for Unity (Point Cloud Free Viewer, PCX)  
Unity can read point cloud files in different formats (xyz and ply) in a single pass  
You can replace start with update in Cloud Manger to refresh the point cloud readings per frame    
**Next step**  
Create a VR observer's camera in the point cloud environment so that the observer can browse the model environment through the VR device.  
Finish writing the lab report with Zhao Xin   
 
**Yinxuan Wu**  
**Completed**  
Read point cloud files of different formats from depth cameras via open3  
Use python to implement point cloud stitching  
Can export point cloud files in a single pass    
**next step**  
Automatically export point cloud files in real time  
Four depth cameras simultaneously shoot in real time without delay  

**Pengkai Wang**  
**Completed**  
Architecture Designing  
Implement point cloud stitching(PointCloud Registration) by using python  
Multi-camera data stream control and export  
Optimize point cloud export efficiency  

**Zhao Xin**  
**Completed**  
Configure the network protocol and environment between the two computers  
Design the program to achieve remote transfer of point cloud files between computer A computer B    
**next step**    
Try to reduce the transmission delay  
Experiment report writing  

**Ding Xintao**  
**Completed**  
HTC Vive and Unity environment configuration  
Select out the appropriate rendering pipeline SRP for Unity  
Problem logging    
**next step**  
Handle point cloud file over bound issue (i.e. read ply file reports error, see professor's RA reply for solution)  
Implement point cloud tracking  


# ECE697SD

Project Proposal Overleaf Link: https://www.overleaf.com/9956381517dgvrjtymdnss

1.点云

1.1 点云拼接（配准）
  
  使用Python第三方库Open3d导出深度相机的点云，并进行拼接（配准）
  RealSense ( librealsenseSDK v2) 已集成到 Open3D (v0.12+) 中，您可以通过 C++ 和 Python API 使用它，而无需librealsense在 Linux、macOS 和 Windows 上单独安装 SDK。英特尔GitHub链接：https://github.com/IntelRealSense/librealsense/tree/master/wrappers/open3d
  Open3D是一个开源库，支持快速开发处理3D数据的软件。Open3D后端是用C++实现的，并通过Python的前端接口公开。Open3D提供了三种数据结构：点云（point cloud）、网格（mesh）和RGB-D图像。对于每个表示，open3D都实现了一整套基本处理算法，如I/O、采样、可视化和数据转换。此外，还包括一些常用的算法，如ICP配准，也就是实现点云拼接的算法。Open3d链接：http://www.open3d.org/docs/latest/tutorial/sensor/index.html

1.2 点云导出：
  目前看来，深度相机本地可视化使用的是视频帧，具体还不明确。

1.3 降低点云分辨率/降采样：
  realsense相机：pyrealsense2.decimation_filter()
  open3d: Voxel downsampling

1.4 点云压缩（powershell脚本压缩后传输）
  
  以下内容仅为拓展学习，不在本项目中实现。
  点云压缩现状及发展趋势 https://blog.csdn.net/baidu_35231778/article/details/116046090
  Google Draco: https://github.com/google/draco
  DracoUnity: https://github.com/atteneder/DracoUnity
  Draco 是一个用于压缩和解压缩 3D 几何网格和点云的库。它旨在改进 3D 图形的存储和传输。Draco 是为压缩效率和速度而设计和制造的。该代码支持压缩点、连接信息、纹理坐标、颜色信息、法线以及与几何相关的任何其他通用属性。使用 Draco，使用 3D 图形的应用程序可以显着缩小而不影响视觉保真度。对于用户来说，这意味着现在可以更快地下载应用程序，可以更快地加载浏览器中的 3D 图形，并且现在可以以一小部分带宽传输 VR 和 AR 场景并快速渲染。Draco 作为 C++ 源代码发布，可用于压缩 3D 图形以及编码数据的 C++ 和 Javascript 解码器。
  ![))QXSHG_X @{$N)Q5}{BENF](https://user-images.githubusercontent.com/35893137/141601448-2afe24d1-2e2a-4bb8-b192-045e106da407.png)
  ![L@Z U }_{VVL0J TPD@8WR](https://user-images.githubusercontent.com/35893137/141601645-3de36fff-7c19-4b37-bb42-f2b424f65364.png)

  几个好用的模型优化库(工具) :
  ● https://github.com/zeux/meshoptimizer 三维模型优化库
  ● https://github.com/zeux/meshoptimizer/tree/master/gltf 在meshoptimizer基础上实现的网格优化程序，可以直接优化gltf模型
  ● github.com/google/draco Google开发的网格压缩库，压缩率非常高
  ● github.com/CesiumGS/glt... Cesium开发的gltf工具，可以直接调用Draco对gltf进行压缩


2.远程传输

  AWS服务器，powershell调用脚本


3.Unity读取点云文件
  
  Unity可以自定义帧数刷新读取xyz格式文件来实现实时读取，但无法读取深度摄像机中点云文件


4.Unity导入VR设备
  
  HTC VIVE，VR Steram与Unity交互


瓶颈和挑战：
  
  1.要实现人物跟踪，需要将人物和场景点云分离，我们只能做到人物作为环境元素来实现观察，通过不断刷新读取点云文件来实现观察人物的位置。
  
  2.Unity实时读取点云文件
  
  3.深度摄像机实时导出点云文件
  
  4.点云文件在A电脑与B电脑之间实时传输  
  

**PS**  
如果要实现人物点云的实时追踪，环境点云和人物点云首先需要分离，同时需要对人物点云进行算法处理，这是一个巨大的挑战。  
尽管RA提供了一些参考资料，但目前看来这些参考资料仅有所关联，并不可以解决这个问题。可能我们不得不花费更多时间探索。


**职责**  

Xiaohao Xia: Develop a project time plan, and communicate with the professor. Import the point cloud file into Unity and implement modeling in Unity at the same time.  

Yinxuan Wu: Responsible for the data capture of the depth camera, Point cloud stitching, read the point cloud file. save hardware, etc.  

Xintao Ding: Responsible for completing the remote transmission of the cloud file with Xin Zhao, preparing the project display, and project record, importing model data into VR headset.  

Xin Zhao: Responsible for develop a software to complete remote transmission of cloud file, and second inspection experiment report.  

**夏晓昊**  
**已完成**  
选取Unity合适的点云读取插件（Point Cloud Free Viewer, PCX）  
Unity可以单次读取不同格式（xyz和ply）的点云文件  
可以通过Cloud Manger的start 更换为update 实现对每帧点云文件读取的刷新    
**下一步**  
在点云环境中创建VR观察者的摄像机，以便观察者可以通过VR设备浏览模型环境。  
和赵鑫完成撰写实验报告   
 
**吴寅轩**  
**已完成**  
通过open3读取深度摄像机不同格式的点云文件  
使用python实现点云拼接  
可以单次导出点云文件    
**下一步**  
自动实时导出点云文件  
四台深度摄像机同时无延迟实时拍摄  

**赵鑫**  
**已完成**  
配置两台电脑之间的网络协议和环境  
设计程序实现电脑A电脑B之间的点云文件远程传输    
**下一步**    
尝试降低传输延迟  
实验报告撰写  

**丁忻涛**  
**已完成**  
HTC Vive和Unity环境配置  
选择出Unity合适的渲染管道SRP  
问题记录    
**下一步**  
处理点云文件过界问题(即读取ply文件报错，解决方案见教授的RA回复)  
实现点云追踪  
    
