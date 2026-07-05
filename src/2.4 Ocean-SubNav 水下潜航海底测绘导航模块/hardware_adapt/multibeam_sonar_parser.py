"""
多波束声呐数据适配接口
底层依赖：Common-LSG io_utils 通用IO工具
功能：解析多波束测深数据，转换为LSG标准截面格式
"""
import numpy as np
from Common_LSG.io_utils import SectionDataStandard

class MultibeamSonarParser(SectionDataStandard):
    def load_bathymetry_data(self, bathy_file_path):
        """加载测深数据文件（xyz/las格式）"""
        data = np.loadtxt(bathy_file_path, delimiter=",")
        x, y, z = data[:,0], data[:,1], data[:,2]
        
        # 测深点云转截面堆叠
        section_stack = self.pointcloud_to_section_stack(
            np.vstack([x,y,z]).T, 
            resolution=1.0
        )
        standard_data = self.format_section_stack(section_stack, spacing=[1.0, 1.0, 1.0])
        return standard_data