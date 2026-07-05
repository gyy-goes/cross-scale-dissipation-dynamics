"""
LSG 通用切片重建内核
全场景通用的非正交切片对齐、多截面融合、三维重建基础逻辑
不包含任何行业专属优化，为所有场景共用的基础工作流
"""

import numpy as np


def non_orthogonal_slice_align(slice_2d, slice_pose, target_space):
    """
    任意角度非正交切片空间对齐
    将任意姿态的二维截面投影对齐到目标三维空间坐标系
    :param slice_2d: 二维截面数据矩阵
    :param slice_pose: 截面位姿字典 origin(3,), normal(3,), u_axis(3,)
    :param target_space: 目标空间尺寸 (H,W,D)
    :return: 对齐后的三维空间截面掩码
    """
    origin = np.array(slice_pose["origin"])
    normal = np.array(slice_pose["normal"])
    u_axis = np.array(slice_pose["u_axis"])
    v_axis = np.cross(normal, u_axis)
    
    # 单位化
    normal = normal / np.linalg.norm(normal)
    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = v_axis / np.linalg.norm(v_axis)
    
    h, w = slice_2d.shape
    volume = np.zeros(target_space)
    
    # 生成截面网格坐标
    u_coords = np.linspace(-w//2, w//2, w)
    v_coords = np.linspace(-h//2, h//2, h)
    uu, vv = np.meshgrid(u_coords, v_coords)
    
    # 二维坐标映射到三维空间
    points_3d = origin + uu[..., np.newaxis] * u_axis + vv[..., np.newaxis] * v_axis
    
    # 离散化到目标体素空间
    coords = np.round(points_3d).astype(int)
    valid = (
        (coords[..., 0] >= 0) & (coords[..., 0] < target_space[0]) &
        (coords[..., 1] >= 0) & (coords[..., 1] < target_space[1]) &
        (coords[..., 2] >= 0) & (coords[..., 2] < target_space[2])
    )
    
    x = coords[valid, 0]
    y = coords[valid, 1]
    z = coords[valid, 2]
    volume[x, y, z] = slice_2d[valid]
    
    return volume


def multi_section_fusion(volume_list, fusion_mode="gradient_weight"):
    """
    多维度截面融合
    将多个不同方向截面对齐后的体数据融合为单一连续场
    :param volume_list: 多个单截面对应的三维体数据
    :param fusion_mode: 融合模式 mean / gradient_weight
    :return: 融合后的三维体数据
    """
    if len(volume_list) == 0:
        return np.array([])
    
    base_shape = volume_list[0].shape
    stacked = np.stack(volume_list, axis=-1)
    
    if fusion_mode == "mean":
        return np.mean(stacked, axis=-1)
    
    elif fusion_mode == "gradient_weight":
        # 梯度加权融合：梯度大的区域权重更高，保留边缘细节
        weights = np.zeros_like(stacked)
        for i in range(stacked.shape[-1]):
            grad = np.gradient(stacked[..., i])
            weights[..., i] = np.sqrt(grad[0]**2 + grad[1]**2 + grad[2]**2)
        weights = weights / (np.sum(weights, axis=-1, keepdims=True) + 1e-8)
        return np.sum(stacked * weights, axis=-1)
    
    else:
        raise ValueError("fusion_mode must be mean or gradient_weight")


def universal_slice_reconstruct(slice_dataset, layer_spacing):
    """
    通用层级切片三维重建主函数
    输入一组有序截面，输出完整三维重建结果
    :param slice_dataset: 截面数据集列表，每项包含 data 二维矩阵 + pose 位姿
    :param layer_spacing: 层间间距
    :return: 三维重建体数据
    """
    aligned_volumes = []
    # 统一目标空间尺寸
    max_h = max(s["data"].shape[0] for s in slice_dataset)
    max_w = max(s["data"].shape[1] for s in slice_dataset)
    depth = len(slice_dataset)
    target_space = (max_h, max_w, depth)
    
    for idx, slice_item in enumerate(slice_dataset):
        # 构造标准位姿（沿Z轴分层）
        pose = {
            "origin": np.array([max_h//2, max_w//2, idx * layer_spacing]),
            "normal": np.array([0, 0, 1]),
            "u_axis": np.array([1, 0, 0])
        }
        vol = non_orthogonal_slice_align(slice_item["data"], pose, target_space)
        aligned_volumes.append(vol)
    
    # 多层融合重建
    result = multi_section_fusion(aligned_volumes, fusion_mode="gradient_weight")
    return result
