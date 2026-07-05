"""
CT DICOM数据适配接口（场景专属）
底层依赖：Common-LSG io_utils 通用IO工具
功能：解析标准DICOM格式CT数据，转换为Common-LSG通用截面输入格式
"""
import numpy as np
from Common_LSG.io_utils import SectionDataStandard

class DicomCTParser(SectionDataStandard):
    SUPPORTED_MODALITY = "CT"

    def load_dicom_series(self, dicom_folder_path):
        """
        加载DICOM序列，提取像素值、层厚、空间坐标信息
        :return: 符合Common-LSG标准的截面数据集
        """
        # 标准DICOM解析逻辑（依赖pydicom，示例核心逻辑）
        try:
            import pydicom
            from pydicom import dcmread
        except ImportError:
            raise ImportError("需安装pydicom依赖：pip install pydicom")

        slices = []
        for file in sorted(os.listdir(dicom_folder_path)):
            if file.endswith(".dcm"):
                ds = dcmread(os.path.join(dicom_folder_path, file))
                if ds.Modality == self.SUPPORTED_MODALITY:
                    slices.append(ds)
        
        # 按层位置排序
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
        
        # 转换为HU值矩阵
        pixel_array = np.stack([s.pixel_array for s in slices])
        hu_array = pixel_array * slices[0].RescaleSlope + slices[0].RescaleIntercept
        
        # 转换为Common-LSG标准截面格式
        standard_data = self.format_section_stack(
            hu_array,
            spacing=slices[0].PixelSpacing + [slices[0].SliceThickness],
            origin=slices[0].ImagePositionPatient
        )
        return standard_data