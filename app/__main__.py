import os


from app.kinect_point_cloud_acquisition import get_single_color_depth_frame
from app.point_cloud import (region_growing, remove_floor_based_on_color_frame,
                             remove_radial_outliers,
                             remove_statistical_outliers, to_point_cloud,
                             visualize_point_cloud)
from app.utilities import (determine_filepath, from_json, save_to_json,
                           write_ply)


def get_highest_recorded_frame_num(dirpath: str) -> int:
    already_recorded_frames = os.listdir(dirpath)
    names = list(map(lambda x: int(x.split('.')[0]), already_recorded_frames))
    highest_recorded_frame_num = max(names) if len(names) > 0 else -1
    return highest_recorded_frame_num + 1


cx=260.166
cy=205.197
fx=367.535
fy=367.535


if __name__ == '__main__':
    save_directory_path = './recorded_frames'

    depth_frame, color_frame = get_single_color_depth_frame((0, 800))
    cloud = to_point_cloud(depth_frame, cx, cy, fx, fy)
    wo_statistical_outliers = remove_statistical_outliers(cloud, 15, 0.04)
    wo_radial_outliers = remove_radial_outliers(cloud, 30, 0.01)
    remove_radial_after_statistical = remove_radial_outliers(wo_statistical_outliers, 30, 0.01)
    remove_statistical_after_radial = remove_statistical_outliers(wo_radial_outliers, 15, 0.04)

    d = {'cloud': cloud, 'wo statistical outliers': wo_statistical_outliers, 'wo radial outliers': wo_radial_outliers,
        'remove radial after stat': remove_radial_after_statistical, 'remove stat after radial': remove_statistical_after_radial}

    visualize_point_cloud(d, 0.01)

    if not os.path.exists(save_directory_path):
       os.makedirs(save_directory_path)

    n = get_highest_recorded_frame_num(save_directory_path)

    write_ply(cloud, f'{save_directory_path}/{n}.basic_cloud.ply')
    write_ply(wo_statistical_outliers, f'{save_directory_path}/{n}.removed_statistical_outliers.ply')
    write_ply(wo_radial_outliers, f'{save_directory_path}/{n}.removed_radial_outliers.ply')
    write_ply(remove_radial_after_statistical, f'{save_directory_path}/{n}.removed_radial_after_statistical_outliers.ply')
    write_ply(remove_statistical_after_radial, f'{save_directory_path}/{n}.removed_statistical_after_radial_outliers.ply')
