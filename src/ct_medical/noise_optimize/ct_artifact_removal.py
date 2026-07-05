"""
CT伪影消除优化模块（场景专属）
底层依赖：Common-LSG constraint_algo 平滑算子
功能：抑制金属伪影、射束硬化伪影，保留组织边缘细节
"""
import numpy as np
from Common_LSG.constraint_algo import GradientSmoother

class CTArtifactOptimizer(GradientSmoother):
    def metal_artifact_removal(self, section_matrix, metal_threshold=2000):
        """
        金属伪影插值修复：识别高密度金属区域，通过周边组织梯度插值补全
        """
        metal_mask = section_matrix >= metal_threshold
        if not np.any(metal_mask):
            return section_matrix
        
        # 调用底层梯度平滑算子做邻域插值
        repaired_matrix = self.gradient_interpolate(section_matrix, metal_mask)
        return repaired_matrix

    def beam_hardening_correction(self, section_stack):
        """
        射束硬化校正：对多截面堆叠做中心-边缘灰度均衡
        """
        corrected_stack = self.radial_gradient_equalize(section_stack)
        return corrected_stack