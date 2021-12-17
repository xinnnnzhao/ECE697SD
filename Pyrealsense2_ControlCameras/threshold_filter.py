## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##                  Export                 ##
#####################################################

# First import the library
import pyrealsense2 as rs
import numpy as np
import math
import os
import open3d as o3d
from open3d.cpu.pybind.visualization import Visualizer
import time
from subprocess import check_output
import subprocess

path = "C:\\Users\\15345\\PycharmProjects\\Pyrealsense_test\\out1.ply"

# state = AppState()

# Declare pointcloud object, for calculating pointclouds and texture mappings
pc = rs.pointcloud()
# We want the points object to be persistent so we can display the last cloud when a frame drops
points = rs.points()


# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()
config = rs.config()
# Enable depth stream

config.enable_stream(rs.stream.depth, rs.format.z16, 30)
other_stream, other_format = rs.stream.color, rs.format.rgb8
config.enable_stream(other_stream, other_format, 30)

# Start streaming with chosen configuration
pipe.start(config)

# profile = pipe.get_active_profile()

##############################################33333333########
threshold_filter = rs.threshold_filter()
threshold_filter.set_option(rs.option.max_distance, 0.8)

# Processing blocks
decimate = rs.decimation_filter()
# decimate.set_option(rs.option.filter_magnitude, 2 ** state.decimate)
decimate.set_option(rs.option.filter_magnitude, 2)

# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
# 我们将使用着色器为我们的 PLY 生成纹理（或者，纹理可以从颜色或红外流中获得）
colorizer = rs.colorizer()

filters = [rs.disparity_transform(),
           rs.spatial_filter(),
           rs.temporal_filter(),
           rs.disparity_transform(False)]

while 1:
    start = time.time()

    # Wait for the next set of frames from the camera
    frames = pipe.wait_for_frames()



    colorized = colorizer.process(frames)


    depth_frame = frames.get_depth_frame().as_video_frame()
    other_frame = frames.first(other_stream).as_video_frame()

    color_image = np.asanyarray(other_frame.get_data())

    # colorized_depth = colorizer.colorize(depth_frame)
    # depth_colormap = np.asanyarray(colorized_depth.get_data())

    # if state.color:
    mapped_frame, color_source = other_frame, color_image
    # else:
    # mapped_frame, color_source = colorized_depth, depth_colormap

    depth_frame = threshold_filter.process(depth_frame)
    depth_frame = decimate.process(depth_frame)


    points = pc.calculate(depth_frame)
    pc.map_to(mapped_frame)

    points.export_to_ply("./pcply.ply", mapped_frame)
    # points.export_to_ply("./pcply2.ply", mapped_frame)

    pcd = o3d.io.read_point_cloud("pcply.ply")
    # downpcd = pcd.voxel_down_sample(voxel_size=0.008)

    o3d.io.write_point_cloud("out1.xyz", pcd)
    # o3d.io.write_point_cloud("out.ply", pcd)

    try:
        os.remove("out.xyz")
        os.rename("out1.xyz", "out.xyz")

        cmd = ["PowerShell", "-ExecutionPolicy", "Unrestricted", "-File", ".\\upload.ps1"]  #
        ec = subprocess.call(cmd)
        print("Powershell returned: {0:d}".format(ec))


    except Exception:
        print("Error: 没有找到文件或读取文件失败")

    end = time.time()
    print('Running time: %s Seconds' % (end - start))


