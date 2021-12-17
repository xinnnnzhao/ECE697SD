# 教程01 可视化点云
import open3d as o3d
import numpy as np

# 本教程的第一部分读取点云并将其可视化。
# The first part of the tutorial reads a point cloud and visualizes it.
print("Load a ply point cloud, print it, and render it")
print("加载ply点云，打印并渲染它")
pcd = o3d.io.read_point_cloud("out.xyz")
o3d.visualization.draw_geometries([pcd])
print(pcd)
print(np.asarray(pcd.points))
o3d.visualization.draw_geometries([pcd],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

# read_point_cloud从文件中读取点云。它尝试根据扩展名解码文件。有关支持的文件类型的列表，请参阅File IO。
#
# draw_geometries可视化点云。使用鼠标/触控板从不同的视点查看几何图形。
# 它看起来像一个密集的表面，但它实际上是一个渲染为面元的点云。GUI 支持各种键盘功能。例如，-键减小点（冲浪）的大小。
# 按H键打印出 GUI 的完整键盘说明列表。有关可视化 GUI 的更多信息，请参阅Customized visualization 自定义可视化。