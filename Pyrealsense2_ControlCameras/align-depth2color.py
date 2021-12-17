## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
from plyfile import PlyData,PlyElement
import plyfile

i = 0

# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
# 创建配置并配置管道以流式传输不同分辨率的颜色和深度流
config = rs.config()

# Get device product line for setting a supporting resolution
# 获取设备产品线设置支持分辨率
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
other_stream, other_format = rs.stream.color, rs.format.rgb8
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
'''
if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
'''


# Start streaming
profile = pipeline.start(config)

# Processing blocks
pc = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude, 2)
colorizer = rs.colorizer()
filters = [rs.disparity_transform(),
           rs.spatial_filter(),
           rs.temporal_filter(),
           rs.disparity_transform(False)]


# Getting the depth sensor's depth scale (see rs-align example for explanation)
# 获取深度传感器的深度刻度（参见 rs-align 示例进行解释）
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)

#####################################################################################################
# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
# 我们将移除超过 clipping_distance_in_meters 米以外的物体的背景
clipping_distance_in_meters = 1  # 1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
# 创建一个对齐对象
# rs.align 允许我们执行深度帧与其他帧的对齐
# “align_to”是我们计划对齐深度帧的流类型。
align_to = rs.stream.color
align = rs.align(align_to)

# Streaming loop
try:
    while True:

        # Get frameset of color and depth
        # 获取颜色和深度的框架集
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image


        # frames.get_depth_frame() 是一个 640x360 的深度图像

        # Align the depth frame to color frame
        # 将深度框与颜色框对齐
        aligned_frames = align.process(frames)

        # Get aligned frames
        # 获取对齐的帧
        aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        

        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        # 验证两帧都有效
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # aligned_depth_frame.

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


        write_ply("C:/Users/15345/PycharmProjects/Pyrealsense_test", depth_image)


        # Remove background - Set pixels further than clipping_distance to grey ##################################################################
        # 移除背景 - 将比 clipping_distance 更远的像素设置为灰色
        grey_color = 153
        #
        depth_image_3d = np.dstack(
            (depth_image, depth_image, depth_image))  # depth image is 1 channel, color is 3 channels

        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        from plyfile import PlyData, PlyElement


        def write_ply(save_path, points, text=True):
            """
            save_path : path to save: '/yy/XX.ply'
            pt: point_cloud: size (N,3)
            """
            points = [(points[i, 0], points[i, 1], points[i, 2]) for i in range(points.shape[0])]
            vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
            el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
            PlyData([el], text=text).write(save_path)



        # depth_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), 0*depth_image, 0*depth_image)
        # color_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), 0*color_image, 0*color_image)

        # Crop_depth_image = np.delete(depth_image, )

        ###############################################################################
        # other_frame = aligned_frames.first(other_stream).as_video_frame()
        # mapped_frame, color_source = other_frame, color_removed          ##############################################################
        # points = pc.calculate(aligned_depth_frame)
        #pc.map_to(mapped_frame)

        # points.export_to_ply("./remove.ply", mapped_frame)
        ###################################################################################



        # Render images 渲染图像:
        #   depth align to color on left 深度与左侧的颜色对齐
        #   depth on right  右侧深度
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        images = np.hstack((bg_removed, depth_colormap))

        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
        if key & 0xFF == ord('E'):
            # pcd = images.export_to_ply("./out%d.ply" % i, bg_removed)
            pcd = images.export_to_ply("./out%d.ply" % i, bg_removed)
            break
finally:
    pipeline.stop()
