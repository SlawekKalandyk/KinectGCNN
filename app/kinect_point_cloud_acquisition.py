import numpy as np
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime


def get_single_frame_from_kinect(depth_range):
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
    depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height
    depth_frame = None

    while(True):
        if kinect.has_new_depth_frame:
            depth_frame = kinect.get_last_depth_frame()
            if not np.any(depth_frame):
                continue

            depth_frame = np.array(list(map(lambda x: 0 if x > depth_range[1] or x < depth_range[0] else x, depth_frame)))
            depth_frame = depth_frame.reshape((depth_height, depth_width)).astype(np.uint16)
            break

    kinect.close()

    return depth_frame