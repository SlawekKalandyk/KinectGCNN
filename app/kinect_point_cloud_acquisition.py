import numpy as np
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import ctypes
import math


def _get_point_in_another_space(points, width, x, y):
    coord = y * width + x - 1
    return points[coord].x, points[coord].y


def get_single_color_depth_frame(depth_range):
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)
    depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height
    color_width, color_height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height
    depth_frame = None
    color_frame = None

    while(True):
        if kinect.has_new_depth_frame and kinect.has_new_color_frame:
            depth_frame = kinect.get_last_depth_frame()
            if not np.any(depth_frame):
                continue

            color_frame = kinect.get_last_color_frame()
            if not np.any(color_frame):
                continue

            depth_frame = np.array(list(map(lambda x: 0 if x > depth_range[1] or x < depth_range[0] else x, depth_frame)))
            depth_frame = depth_frame.reshape((depth_height, depth_width)).astype(np.uint16)
            color_frame = color_frame.reshape((color_height, color_width, 4))
            break

    kinect.close()

    depth2color_points_type = PyKinectV2._ColorSpacePoint * np.int(depth_width * depth_height)
    depth2color_points = ctypes.cast(depth2color_points_type(), ctypes.POINTER(PyKinectV2._ColorSpacePoint))
    kinect._mapper.MapDepthFrameToColorSpace(ctypes.c_uint(depth_width * depth_height), kinect._depth_frame_data, ctypes.c_uint(depth_width * depth_height), depth2color_points)

    rescaled_color_frame = []
    for i in range(0, depth_height):
        row = []
        for j in range(0, depth_width):
            x, y = _get_point_in_another_space(depth2color_points, depth_width, j, i)
            if x >=0 and y >= 0 and y < color_height and x < color_width:
                bgr_row = list(color_frame[int(math.floor(y + 0.5)), int(math.floor(x + 0.5))])
                rgb_row = [bgr_row[2], bgr_row[1], bgr_row[0], bgr_row[3]]
                row.append(rgb_row)
            else:
                row.append([0, 0, 0, 0])
        rescaled_color_frame.append(row) 

    rescaled_color_frame = np.asarray(rescaled_color_frame)

    for i in range(0, depth_height):
        for j in range(0, depth_width):
            if not depth_frame[i, j]:
                rescaled_color_frame[i, j] = [0, 0, 0, 0]

    return depth_frame, rescaled_color_frame