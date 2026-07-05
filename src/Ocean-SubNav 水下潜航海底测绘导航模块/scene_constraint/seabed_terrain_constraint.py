"""
海底地形约束模块（场景专属）
底层依赖：Common-LSG constraint_algo 基类
功能：基于海底地貌梯度约束，适配水下声呐测绘特性
"""
from Common_LSG.constraint_algo import BaseSectionConstraint

class SeabedTerrainConstraint(BaseSectionConstraint):
    MAX_SEABED_SLOPE = 45  # 海底地形最大坡度约束

    def seabed_slope_constrain(self, bathymetry_section):
        """
        海底坡度约束：限制地形梯度突变，符合海底沉积地貌规律
        """
        constrained_section = self.gradient_limit_constrain(
            bathymetry_section,
            max_gradient=np.tan(np.radians(self.MAX_SEABED_SLOPE))
        )
        return constrained_section

    def water_depth_layer_constrain(self, section_stack, max_depth):
        """水深分层约束，适配声呐回波层级积分"""
        layered_stack = self.layer_interval_constrain(section_stack, 0, max_depth, layer_num=30)
        return layered_stack