"""
声呐散射噪声抑制模块（场景专属）
底层依赖：Common-LSG constraint_algo 平滑算子
功能：抑制水体散射、多途反射噪声，提升海底地形识别精度
"""
from Common_LSG.constraint_algo import AdaptiveSmoother

class SonarScatterDenoise(AdaptiveSmoother):
    def water_column_noise_suppress(self, sonar_section):
        """
        水体柱散射噪声抑制：去除水体中悬浮颗粒、气泡产生的噪声
        """
        denoised_section = self.vertical_adaptive_filter(sonar_section, filter_type="median")
        return denoised_section

    def multipath_artifact_remove(self, sonar_stack):
        """多途反射伪影消除"""
        cleaned_stack = self.reflection_artifact_filter(sonar_stack)
        return cleaned_stack