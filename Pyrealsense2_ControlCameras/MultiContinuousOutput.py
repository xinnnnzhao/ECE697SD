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
import time
from subprocess import check_output
import subprocess
import copy

def preprocess_point_cloud(pcd, voxel_size):
    # Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    # Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    # Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh
def prepare_dataset(voxel_size):
    # Load two point clouds and disturb initial pose.")
    source = o3d.io.read_point_cloud("pcply1.ply")
    target = o3d.io.read_point_cloud("pcply2.ply")
    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source, target, source_down, target_down, source_fpfh, target_fpfh
def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    # RANSAC registration on downsampled point clouds.")
    # Since the downsampling voxel size is %.3f," % voxel_size)
    # we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999))
    return result
def refine_registration(source, target, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 0.4
    # Point-to-plane ICP registration is applied on original point")
    # clouds to refine the alignment. This time we use a strict")
    # distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_icp(
        source, target, distance_threshold, result_ransac.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    return result



# Declare pointcloud object, for calculating pointclouds and texture mappings
pc_1 = rs.pointcloud()
pc_2 = rs.pointcloud()
# We want the points object to be persistent so we can display the last cloud when a frame drops
points_1 = rs.points()
points_2 = rs.points()

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe_1 = rs.pipeline()
config_1 = rs.config()
# Enable depth stream
config_1.enable_device('031522070137')
config_1.enable_stream(rs.stream.depth, rs.format.z16, 30)
config_1.enable_stream(rs.stream.color, rs.format.rgb8, 30)

pipe_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device('026322070647')
config_2.enable_stream(rs.stream.depth, rs.format.z16, 30)
config_2.enable_stream(rs.stream.color, rs.format.bgr8, 30)


# Start streaming with chosen configuration
pipe_1.start(config_1)
pipe_2.start(config_2)

# profile = pipe.get_active_profile()

##############################################33333333########
threshold_filter = rs.threshold_filter()
threshold_filter.set_option(rs.option.max_distance, 2)

# Processing blocks
decimate = rs.decimation_filter()
# decimate.set_option(rs.option.filter_magnitude, 2 ** state.decimate)
decimate.set_option(rs.option.filter_magnitude, 8)

# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
# 我们将使用着色器为我们的 PLY 生成纹理（或者，纹理可以从颜色或红外流中获得）
colorizer_1 = rs.colorizer()
colorizer_2 = rs.colorizer()

while 1:
    start = time.time()

    # Wait for the next set of frames from the camera
    frames_1 = pipe_1.wait_for_frames()
    colorized_1 = colorizer_1.process(frames_1)
    frames_2 = pipe_2.wait_for_frames()
    colorized_2 = colorizer_2.process(frames_2)

    depth_frame_1 = frames_1.get_depth_frame()
    color_frame_1 = frames_1.get_color_frame()
    depth_frame_2 = frames_2.get_depth_frame()
    color_frame_2 = frames_2.get_color_frame()

    depth_frame_1 = threshold_filter.process(depth_frame_1)
    depth_frame_1 = decimate.process(depth_frame_1)
    depth_frame_2 = threshold_filter.process(depth_frame_2)
    depth_frame_2 = decimate.process(depth_frame_2)

    points_1 = pc_1.calculate(depth_frame_1)
    pc_1.map_to(color_frame_1)
    points_2 = pc_2.calculate(depth_frame_2)
    pc_2.map_to(color_frame_2)

    points_1.export_to_ply("./pcply1.ply", color_frame_1)
    points_2.export_to_ply("./pcply2.ply", color_frame_2)
###############################################################################################
    voxel_size = 0.05  # means 5cm for this dataset
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(
        voxel_size)

    result_ransac = execute_global_registration(source_down, target_down,
                                                source_fpfh, target_fpfh,
                                                voxel_size)
    source.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    target.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    result_icp = refine_registration(source, target, source_fpfh, target_fpfh,
                                     voxel_size)
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.transform(result_icp.transformation)
    pcd = source_temp + target_temp
    o3d.io.write_point_cloud("out1.xyz", pcd)
###########################################################################

    try:
        os.remove("out.xyz")
        os.rename("out1.xyz", "out.xyz")

        #cmd = ["PowerShell", "-ExecutionPolicy", "Unrestricted", "-File", ".\\upload.ps1"]  #
        #ec = subprocess.call(cmd)
        #print("Powershell returned: {0:d}".format(ec))


    except Exception:
        print("Error: 没有找到文件或读取文件失败")

    end = time.time()
    print('Running time: %s Seconds' % (end - start))