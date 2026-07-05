"""
地震剖面/测井数据适配接口
底层依赖：Common-LSG io_utils 通用IO工具
功能：解析地震SEG-Y数据、测井数据，转换为标准截面格式
"""
import numpy as np
from Common_LSG.io_utils import SectionDataStandard

class SeismicLoggingParser(SectionDataStandard):
    def load_segy_section(self, segy_path):
        """加载SEG-Y格式地震剖面数据"""
        try:
            import segyio
        except ImportError:
            raise ImportError("需安装segyio依赖：pip install segyio")
        
        with segyio.open(segy_path, "r") as f:
            seismic_data = np.array([f.trace[i] for i in range(f.tracecount)])
        
        standard_data = self.format_section_stack(
            np.expand_dims(seismic_data, axis=0),
            spacing=[1.0, 0.004, 1.0],
            origin=[0, 0, 0]
        )
        return standard_data