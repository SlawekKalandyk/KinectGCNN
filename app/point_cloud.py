import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d
import os
import tempfile
from math import sqrt

def to_point_cloud(depth, cx, cy, fx, fy) -> np.ndarray:
    rows, cols = depth.shape
    c, r = np.meshgrid(np.arange(cols), np.arange(rows), sparse=True)
    valid = (depth > 0) & (depth < 4500)
    z = np.where(valid, depth / 1000, np.nan)
    x = np.where(valid, z * (c - cx) / fx, 0)
    y = np.where(valid, z * (r - cy) / fy, 0)
    cloud_3d = np.dstack((x, y, z))
    depth_cloud = cloud_3d.reshape((rows * cols, 3))
    depth_cloud = np.array(list(filter(lambda x: not np.isnan(x)[2], depth_cloud)))

    return depth_cloud


def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])


def _set_axes_equal(ax: plt.Axes):
    ax.set_box_aspect([1,1,1])
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)


def visualize_point_cloud(point_clouds, point_visual_size):
    i = 1
    for point_cloud in point_clouds:
        plt.figure(i)
        ax = plt.axes(projection='3d')
        ax.scatter(point_cloud[:,0], point_cloud[:,1], point_cloud[:,2], s=point_visual_size)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        i += 1
        _set_axes_equal(ax)
    plt.show()


def remove_outliers(point_cloud, neighbours, std) -> (np.ndarray, np.ndarray):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)

    cl, _ = pcd.remove_statistical_outlier(neighbours, std)
    
    return np.asarray(cl.points)


def _point_distance_3d(point1, point2):
    sum = 0
    for i in range(0, 3):
        sum += (point2[i] - point1[i]) ** 2
    return sqrt(sum)


def _traverse_ring(ring, new_object, rings, traversed_rings):
    new_object.append(ring)
    traversed_rings.append(ring)
    for child_ring in rings[ring]:
        _traverse_ring(child_ring, new_object, rings, traversed_rings)


def region_growing(point_cloud, radius) -> np.ndarray:
    # { (x, y, z): [[a, b, c], ...]}
    rings = {}
    # create a ring on point iteration
    # add only new points to existing rings
    for point in point_cloud:
        point_as_tuple = tuple(point)
        rings[point_as_tuple] = []
        for ring in rings:
            if point_as_tuple == ring:
                continue
            elif _point_distance_3d(point_as_tuple, ring) < radius:
                rings[ring].append(point_as_tuple)
                break

    objects = []
    traversed_rings = []

    for ring in rings:
        if ring in traversed_rings:
            continue
        else:
            new_object = []
            _traverse_ring(ring, new_object, rings, traversed_rings)
            objects.append(new_object)

    objects.sort(key=lambda x: len(x), reverse=True)
    return np.asarray(objects[0])