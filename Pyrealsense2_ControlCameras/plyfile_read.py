from plyfile import PlyData,PlyElement
import numpy as np

def read_ply(filename):
    """ read XYZ point cloud from filename PLY file """
    plydata = PlyData.read(filename)
    x = np.asarray(plydata.elements[0].data['x'])
    y = np.asarray(plydata.elements[0].data['y'])
    z = np.asarray(plydata.elements[0].data['z'])
    return np.stack([x,y,z], axis=1)

ply = read_ply("iPhone2.ply")


def write_ply(save_path, points, text=True):
    """
    输入点云数据，并写入一个*.ply文件
    :param save_path: 文件路径 + *.ply
    :param points:
    :param text:
    :return:
    """
    points = [(points[i, 0], points[i, 1], points[i, 2]) for i in range(points.shape[0])]
    vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
    PlyData([el], text=text).write(save_path)

write_ply("C:/Users/15345/PycharmProjects/Pyrealsense_test", ply)
