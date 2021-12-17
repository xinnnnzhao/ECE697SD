import numpy as np
import pyrealsense2 as rs
import open3d as o3d

if __name__ == "__main__":
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # Start streaming
    pipeline.start(config)
    # 深度图像向彩色对齐
    align_to_color = rs.align(rs.stream.color)

    try:
        pc = rs.pointcloud()
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        frames = align_to_color.process(frames)

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            print("wrong!")
            # Convert images to numpy arrays
            pc.map_to(color_frame)
        points = pc.calculate(depth_frame)
        print("points", type(points), points)

        vtx = np.asanyarray(points.get_vertices())
        print(vtx.shape)
        npy_vtx = np.zeros((len(vtx), 3), float)
        for i in range(len(vtx)):
            npy_vtx[i][0] = np.float(vtx[i][0])
            npy_vtx[i][1] = np.float(vtx[i][1])
            npy_vtx[i][2] = -np.float(vtx[i][2])
        print("npy_vtx", npy_vtx.shape, npy_vtx)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(npy_vtx)
        # 显示点云
        o3d.visualization.draw_geometries([pcd])

    finally:
        # Stop streaming
        pipeline.stop()
