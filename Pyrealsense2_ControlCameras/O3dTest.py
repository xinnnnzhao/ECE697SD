import open3d as o3d
import json
import math
import ctypes
import pyglet

import pyglet.gl as gl
import numpy as np
import pyrealsense2 as rs

import time

o3d.t.io.RealSenseSensor.list_devices()
# o3d.t.io.RealSenseSensor.capture_frame()

'''
with open(config_filename) as cf:
    rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

rs = o3d.t.io.RealSenseSensor()
rs.init_sensor(rs_cfg, 0, bag_filename)
rs.start_capture(True)  # true: start recording with capture
for fid in range(150):
    im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
    # process im_rgbd.depth and im_rgbd.color

rs.stop_capture()
'''

# Configure streams
pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, rs.format.z16, 30)
other_stream, other_format = rs.stream.color, rs.format.rgb8
config.enable_stream(other_stream, other_format, 30)

# Start streaming
pipeline.start(config)
profile = pipeline.get_active_profile()

depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
w, h = depth_intrinsics.width, depth_intrinsics.height

# Processing blocks
pc = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude)
colorizer = rs.colorizer()
filters = [rs.disparity_transform(),
           rs.spatial_filter(),
           rs.temporal_filter(),
           rs.disparity_transform(False)]

