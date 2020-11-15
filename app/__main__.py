from app.kinect_point_cloud_acquisition import get_single_frame_from_kinect
from app.point_cloud import to_point_cloud, remove_outliers, visualize_point_cloud
from app.utilities import save_to_json, determine_filepath, from_json
import open3d as o3d
import numpy
from threading import Thread

cx=260.166
cy=205.197
fx=367.535
fy=367.535

if __name__ == '__main__':
    save_dir = '../saved_data'
    item_name = 'keyboard'

    depth_frame = get_single_frame_from_kinect((0, 1000))
    depth_cloud = to_point_cloud(depth_frame, cx, cy, fx, fy)
    cloud_without_outliers = remove_outliers(depth_cloud)
    visualize_point_cloud((depth_cloud, cloud_without_outliers))
    
    #filepath = determine_filepath(save_dir, item_name)
    #save_to_json(filepath, depth_cloud)