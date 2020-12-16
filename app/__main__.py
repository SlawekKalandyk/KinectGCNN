from app.kinect_point_cloud_acquisition import get_single_color_depth_frame
from app.point_cloud import to_point_cloud, remove_statistical_outliers, remove_radial_outliers, remove_floor_based_on_color_frame, visualize_point_cloud, region_growing
from app.utilities import save_to_json, determine_filepath, from_json
import open3d as o3d
import numpy as np
from threading import Thread
import os
import pathlib
from matplotlib import pyplot as plt
import PIL as pil


cx=260.166
cy=205.197
fx=367.535
fy=367.535


if __name__ == '__main__':
    depth_frame, color_frame = get_single_color_depth_frame((0, 700))
    depth_frame = remove_floor_based_on_color_frame(depth_frame, color_frame, (220, 240), (220, 240), (220, 240))

    plt.figure()
    plt.imshow(color_frame)
    plt.show()

    cloud = to_point_cloud(depth_frame, cx, cy, fx, fy)
    wo_statistical_outliers = remove_statistical_outliers(cloud, 15, 0.04)
    wo_radial_outliers = remove_radial_outliers(cloud, 30, 0.01)
    remove_radial_after_statistical = remove_radial_outliers(wo_statistical_outliers, 15, 0.05)
    visualize_point_cloud((cloud, wo_statistical_outliers, wo_radial_outliers, remove_radial_after_statistical), 0.01)

    # colors = from_json('color.json')
    # plt.imshow(colors, interpolation='nearest')
    # plt.show()
    # cloud = to_point_cloud(from_json('depth.json'), cx, cy, fx, fy)
    # visualize_point_cloud([cloud], 0.02)

    # clouds = []
    # for directory in os.listdir(save_dir_2):
    #     if directory == 'cup':
    #         for item in os.listdir(save_dir_2 + '/' + directory):
    #             item_path = save_dir_2 + '/' + directory + '/' + item
    #             cloud = from_json(item_path)
    #             clouds.append(cloud)
    # visualize_point_cloud(clouds, 0.02)
    