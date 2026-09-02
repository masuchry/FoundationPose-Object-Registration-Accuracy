"""Estimated pose via the eye-in-hand chain:
   T_base_obj = T_base_tcp @ T_tcp_cam @ T_cam_obj   (4x4 transforms, mm)."""

import numpy as np

# Robot base -> TCP (robot forward kinematics)
T_base_tcp = np.array([
    [-0.9065, -0.4218, -0.0159,  54.39],
    [-0.4218,  0.9067, -0.0061, 515.58],
    [ 0.0170,  0.0011, -0.9999,  88.76],
    [ 0.0,     0.0,     0.0,      1.0],
])

# TCP -> camera
T_tcp_cam = np.array([
    [ 0.0,  1.0,  0.0, 0.0],
    [-1.0,  0.0,  0.0, 0.0],
    [ 0.0,  0.0,  1.0, 8.3],
    [ 0.0,  0.0,  0.0, 1.0],
])

# camera -> object (FoundationPose output)
T_cam_obj = np.array([
    [-0.903,  0.002, -0.429,  -6.77],
    [-0.429, -0.001,  0.903,  46.49],
    [ 0.002,  0.999,  0.001, 246.24],
    [ 0.0,    0.0,    0.0,     1.0],
])

# Estimated object pose in the base frame
T_ep = T_base_tcp @ T_tcp_cam @ T_cam_obj

np.set_printoptions(suppress=True, precision=4)
print(T_ep)
