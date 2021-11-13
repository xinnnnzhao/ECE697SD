# ECE697SD

Project Proposal Overleaf Link: https://www.overleaf.com/9956381517dgvrjtymdnss

1.点云

1）点云拼接（配准）
  使用Python第三方库Open3d导出深度相机的点云，并进行拼接（配准）
  RealSense ( librealsenseSDK v2) 已集成到 Open3D (v0.12+) 中，您可以通过 C++ 和 Python API 使用它，而无需librealsense在 Linux、macOS 和 Windows 上单独安装 SDK。英特尔GitHub链接：https://github.com/IntelRealSense/librealsense/tree/master/wrappers/open3d
  Open3D是一个开源库，支持快速开发处理3D数据的软件。Open3D后端是用C++实现的，并通过Python的前端接口公开。Open3D提供了三种数据结构：点云（point cloud）、网格（mesh）和RGB-D图像。对于每个表示，open3D都实现了一整套基本处理算法，如I/O、采样、可视化和数据转换。此外，还包括一些常用的算法，如ICP配准，也就是实现点云拼接的算法。Open3d链接：http://www.open3d.org/docs/latest/tutorial/sensor/index.html

2）点云导出
  目前看来，深度相机本地可视化使用的是视频帧，具体还不明确。

3）点云压缩  
  点云压缩现状及发展趋势 https://blog.csdn.net/baidu_35231778/article/details/116046090


3.远程传输

  AWS服务器，shell调用脚本


4.Unity读取点云文件
  
  Unity可以读取ply格式文件，但无法读取深度摄像机中点云文件


5.Unity导入VR设备
  
  HTC VIVE，VR Steram与Unity交互


瓶颈和挑战
  
  1.要实现人物跟踪，需要将人物和场景点云分离，我们只能做到人物作为环境元素来实现观察，通过不断刷新读取点云文件来实现观察人物的位置。
  
  2.Unity实时读取点云文件
  
  3.深度摄像机实时导出点云文件
  
  4.点云文件在A电脑与B电脑之间实时传输
  

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
如果要实现人物点云的实时追踪，环境点云和人物点云首先需要分离，同时需要对人物点云进行算法处理，这是一个巨大的挑战，我们可能需要使用其他方式替换处理。
Unity自动实时读取点云文件，当Unity第一次读取时仍需要手动读取，需要设计脚本

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

