import transforms3d as t3d  # pip install transform3d
import open3d as o3d  # pip install open3d-python==0.5
import numpy as np
import math

# load point cloud
i = 4
depth_image_path = "../output/bop_data/lmo/train_pbr/000000/depth/000000.png"
depth_raw = o3d.io.read_image(depth_image_path)
image_width = 671
image_height = 502
fx = 1122.375
fy = 1122.375
cx = 334.4445
cy = 264.443075

intrinsic = o3d.camera.PinholeCameraIntrinsic(
    image_width, image_height, fx, fy, cx, cy)
extrinsic = np.identity(4)
print(extrinsic)
depth_scale = 10
depth_trunc = 1500.0

np_depth = np.array(depth_raw)
depth_raw = o3d.geometry.Image(np_depth)
print(depth_raw)
print(type(depth_raw))
print(type(intrinsic))

color = True

pcd = o3d.geometry.PointCloud.create_from_depth_image(
    depth=depth_raw, intrinsic=intrinsic, extrinsic=extrinsic,
    depth_scale=depth_scale, depth_trunc=depth_trunc, stride=int(1))
if not color:
    pcd.paint_uniform_color([0, 255, 0])

# compose transform matrix
T = [20, 30, 40]
R = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]  # rotation matrix
Z = [1.0, 1.0, 1.0]  # zooms
A = t3d.affines.compose(T, R, Z)
print(A)

# rotation matrix to euler
rx, ry, rz = t3d.euler.mat2euler(R, axes='sxyz')
print(rx, ry, rz)

# euler to rotation matrix
R1 = t3d.euler.euler2mat(rx, ry, rz, axes='sxyz')
print(R1.astype(float))

# visualization, x, y, z axis will be rendered as red, green, and blue
base_coordinate = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1000)
coordinate1 = o3d.geometry.TriangleMesh.create_coordinate_frame(size=500)
coordinate2 = o3d.geometry.TriangleMesh.create_coordinate_frame(size=300)

# r_xyz = np.array([180.272, 9.67795, 270.592]) # camera in base pose
# r_xyz = r_xyz/180*math.pi
R_1 = np.array([[0.010182, -0.999944, 0.003005],
                [-0.985716, -0.009532, 0.168148],
                [-0.168110, -0.004674, -0.985757]])
T_1 = np.array([393.100000, -280.894000, 1338.030000])
H_1 = t3d.affines.compose(T_1, R_1, Z)  # camera in base pose
rx_1, ry_1, rz_1 = t3d.euler.mat2euler(R_1, axes='sxyz')
r_xyz_1 = np.array([rx_1, ry_1, rz_1])/math.pi*180
print("camera in base matrix:{}".format(H_1))
print("rx_1, ry_1, rz_1:{}".format(r_xyz_1))
# coordinate1.transform(H_1)


Arrays = [
    np.array([[0, 1, 0],
                [1, 0, 0],
                [0, 0, -1]]),
    np.array([[0, 1, 0],
                [-1, 0, 0],
                [0, 0, -1]]),
    np.array([[0, -1, 0],
                [1, 0, 0],
                [0, 0, -1]]),
    np.array([[0, -1, 0],
                [-1, 0, 0],
                [0, 0, -1]]),
    np.array([[1, 0, 0],
                [0, 1, 0],
                [0, 0, -1]]),
    np.array([[1, 0, 0],
                [0, -1, 0],
                [0, 0, -1]]),
    np.array([[-1, 0, 0],
                [0, 1, 0],
                [0, 0, -1]]),
    np.array([[-1, 0, 0],
                [0, -1, 0],
                [0, 0, -1]]),
]

# 0 1 1 0
# 0 1 -1 0
# 0 -1 1 0
# 0 -1 -1 0
# 1 0 0 1
# 1 0 0 -1
# -1 0 0 1
# -1 0 0 -1
R_2in1 = Arrays[i]

R_2 = R_1.dot(R_2in1)
H_2 = t3d.affines.compose(T_1, R_2, Z)
coordinate2.transform(H_2)

# draw
# pcd.transform(np.linalg.inv(H_1))
rx_2, ry_2, rz_2 = t3d.euler.mat2euler(R_2, axes='sxyz')
print("rx_2, ry_2, rz_2:{},{},{}".format(rx_2, ry_2, rz_2))
H3 = np.linalg.inv(H_1)
coordinate1.transform(H3)
o3d.visualization.draw_geometries([base_coordinate, pcd, coordinate1])


