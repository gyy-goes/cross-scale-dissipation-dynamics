"""
LSG 基础约束算法
全场景通用的噪声平滑、坐标校准、畸变修正
不含行业专属优化，为所有领域共用的基础校正能力
"""

import numpy as np
from scipy.ndimage import gaussian_filter


def general_noise_smooth(data, sigma=1.0, mode="gaussian"):
    """
    通用噪声平滑约束
    :param data: 输入二维/三维数据
    :param sigma: 平滑强度
    :param mode: 平滑算法 gaussian / median
    :return: 平滑后数据
    """
    if mode == "gaussian":
        return gaussian_filter(data, sigma=sigma)
    elif mode == "median":
        from scipy.ndimage import median_filter
        return median_filter(data, size=int(sigma*2+1))
    else:
        raise ValueError("mode must be gaussian or median")


def global_coordinate_calibrate(points, reference_points):
    """
    全局坐标校准
    通过参考点对齐，将局部截面坐标校准到全局统一坐标系
    :param points: 待校准点集 (N, 3)
    :param reference_points: 参考点集 (M, 3)，至少3个非共线点
    :return: 校准后点集, 变换矩阵
    """
    # 计算质心
    centroid_p = np.mean(points, axis=0)
    centroid_r = np.mean(reference_points, axis=0)
    
    # 去中心化
    p_centered = points - centroid_p
    r_centered = reference_points - centroid_r
    
    # SVD求解最优旋转矩阵
    H = p_centered.T @ r_centered
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    
    # 保证右手坐标系
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T
    
    t = centroid_r - R @ centroid_p
    
    # 应用变换
    calibrated = (R @ points.T).T + t
    transform = np.eye(4)
    transform[:3, :3] = R
    transform[:3, 3] = t
    
    return calibrated, transform


def geometry_distortion_correct(section_data, distortion_coeffs):
    """
    通用几何畸变修正
    :param section_data: 截面二维数据
    :param distortion_coeffs: 畸变系数 [k1, k2, p1, p2]
    :return: 校正后截面数据
    """
    h, w = section_data.shape
    k1, k2, p1, p2 = distortion_coeffs
    
    # 生成归一化坐标
    x = np.linspace(-1, 1, w)
    y = np.linspace(-1, 1, h)
    xx, yy = np.meshgrid(x, y)
    
    r2 = xx**2 + yy**2
    r4 = r2**2
    
    # 径向畸变
    x_distorted = xx * (1 + k1 * r2 + k2 * r4)
    y_distorted = yy * (1 + k1 * r2 + k2 * r4)
    
    # 切向畸变
    x_distorted += 2 * p1 * xx * yy + p2 * (r2 + 2 * xx**2)
    y_distorted += p1 * (r2 + 2 * yy**2) + 2 * p2 * xx * yy
    
    # 映射回像素坐标
    map_x = (x_distorted + 1) * (w - 1) / 2
    map_y = (y_distorted + 1) * (h - 1) / 2
    
    # 重采样校正
    from scipy.ndimage import map_coordinates
    corrected = map_coordinates(section_data, [map_y.ravel(), map_x.ravel()], order=1)
    return corrected.reshape(h, w)
