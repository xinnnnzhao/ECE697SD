# Auther: Yinxuan Wu

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

###########################################################################
depth_to_disparity = rs.disparity_transform(True)
disparity_to_depth = rs.disparity_transform(False)

# Processing blocks
decimate = rs.decimation_filter()
# decimate.set_option(rs.option.filter_magnitude, 2 ** state.decimate)
decimate.set_option(rs.option.filter_magnitude, 4)

# Spatial Filter is a fast implementation of
# Domain-Transform Edge Preserving Smoothing
spatial = rs.spatial_filter()
# We can emphesize the effect of the filter by
# cranking-up smooth_alpha and smooth_delta options:
spatial.set_option(rs.option.filter_magnitude, 2)
spatial.set_option(rs.option.filter_smooth_alpha, 0.5)
spatial.set_option(rs.option.filter_smooth_delta, 20)
spatial.set_option(rs.option.holes_fill, 0)
# The filter also offers some basic spatial hole filling capabilities:
spatial.set_option(rs.option.holes_fill, 3)

# Next, we need to "feed" the frames to the filter one by one:
temporal = rs.temporal_filter()

# 孔填充过滤器提供了附加的深度外推层：
hole_filling = rs.hole_filling_filter()
################################################################################

# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
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

    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    depth_frame = decimate.process(depth_frame)
    depth_frame = depth_to_disparity.process(depth_frame)
    # depth_frame = spatial.process(depth_frame)
    depth_frame = temporal.process(depth_frame)
    depth_frame = disparity_to_depth.process(depth_frame)
    # depth_frame = hole_filling.process(depth_frame)

    color_image = np.asanyarray(color_frame.get_data())

    mapped_frame, color_source = color_frame, color_image

    depth_frame = decimate.process(depth_frame)
    
    #######################################################################################################
    # depth_image_3d = np.dstack(
    #    (depth_image, depth_image, depth_image))  # depth image is 1 channel, color is 3 channels

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
        
        #####################################################
        # cmd = ["PowerShell", "-ExecutionPolicy",          #
        #       "Unrestricted", "-File", ".\\upload.ps1"]   #
        # ec = subprocess.call(cmd)                         #
        # print("Powershell returned: {0:d}".format(ec))    #
        #####################################################

    except Exception:
        print("Error: 没有找到文件或读取文件失败")


    end = time.time()
    print('Running time: %s Seconds' % (end - start))




'''    
    # Create save_to_ply object
    ply = rs.save_to_ply("1.ply")

    # Set options to the desired values
    # In this example we'll generate a textual PLY with normals (mesh is already created by default)
    # 将选项设置为所需的值
    # 在这个例子中，我们将生成一个带有法线的文本层（默认情况下已经创建了网格）
    ply.set_option(rs.save_to_ply.option_ply_binary, False)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    print("Saving to 1.ply...")
    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)
    
    
    finally:
    pipe.stop()
'''
