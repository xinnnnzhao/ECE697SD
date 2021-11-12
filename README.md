# ECE697SD

Project Proposal Overleaf Link: https://www.overleaf.com/9956381517dgvrjtymdnss

1.点云拼接（配准）
  使用Python第三方库Open3d导出深度相机的点云，并进行拼接（配准）
  RealSense ( librealsenseSDK v2) 已集成到 Open3D (v0.12+) 中，您可以通过 C++ 和 Python API 使用它，而无需librealsense在 Linux、macOS 和 Windows 上单独安装 SDK。英特尔GitHub链接：https://github.com/IntelRealSense/librealsense/tree/master/wrappers/open3d
  Open3D是一个开源库，支持快速开发处理3D数据的软件。Open3D后端是用C++实现的，并通过Python的前端接口公开。Open3D提供了三种数据结构：点云（point cloud）、网格（mesh）和RGB-D图像。对于每个表示，open3D都实现了一整套基本处理算法，如I/O、采样、可视化和数据转换。此外，还包括一些常用的算法，如ICP配准，也就是实现点云拼接的算法。Open3d链接：http://www.open3d.org/docs/latest/tutorial/sensor/index.html

2.点云导出
  目前看来，深度相机本地可视化使用的是视频帧，具体还不明确。

3.远程传输

4.Unity读取点云文件
  Unity可以读取ply格式文件，但无法读取深度摄像机中点云文件

5.Unity导入VR设备
  HTC VIVE，VR Steram与Unity交互

瓶颈和挑战
  1.要实现人物跟踪，需要将人物和场景点云分离，我们只能做到人物作为环境元素来实现观察，通过不断刷新读取点云文件来实现观察人物的位置。
  2.Unity实时读取点云文件
  3.深度摄像机实时导出点云文件
  4.点云文件在A电脑与B电脑之间实时传输
