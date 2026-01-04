"""
报表生成模块
负责生成Excel报表
"""

import pandas as pd
from pathlib import Path
from typing import Dict
from loguru import logger


class ReportGenerator:
    """报表生成器"""

    def __init__(self, config: Dict):
        """
        初始化报表生成器

        Args:
            config: 配置字典
        """
        self.config = config
        self.output_dir = Path(config['output']['directory'])
        self.output_filename = config['output']['filename']

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self,
                       df2: pd.DataFrame,
                       df1_processed: pd.DataFrame,
                       pivot_df: pd.DataFrame) -> Path:
        """
        生成完整的Excel报表

        Sheet结构:
        1. 2025122911704000480: 表格2原始数据
        2. 计算解决率过程数据（调整后）: 表格1处理后数据
        3. 计算解决率: 透视表结果

        Args:
            df2: 表格2原始数据
            df1_processed: 表格1处理后数据
            pivot_df: 透视表结果

        Returns:
            Path: 输出文件路径
        """
        output_path = self.output_dir / self.output_filename

        logger.info(f"开始生成报表: {output_path}")

        # 使用ExcelWriter写入多个Sheet
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet1: 原始数据
            df2.to_excel(writer, sheet_name='2025122911704000480', index=False)
            logger.info(f"写入Sheet1 '2025122911704000480': {len(df2)}行")

            # Sheet2: 处理后数据
            df1_processed.to_excel(writer, sheet_name='计算解决率过程数据（调整后）', index=False)
            logger.info(f"写入Sheet2 '计算解决率过程数据（调整后）': {len(df1_processed)}行")

            # Sheet3: 透视表
            pivot_df.to_excel(writer, sheet_name='计算解决率')
            logger.info(f"写入Sheet3 '计算解决率': {len(pivot_df)}行")

        # 获取文件大小
        file_size = output_path.stat().st_size / 1024  # KB

        logger.info(f"""
        报表生成成功 ✓
        - 文件路径: {output_path}
        - 文件大小: {file_size:.2f} KB
        - Sheet数量: 3
        """)

        return output_path

    def format_report(self, file_path: Path):
        """
        格式化Excel报表(添加样式、格式化等)

        Args:
            file_path: Excel文件路径
        """
        logger.info("开始格式化报表...")

        # TODO: 实现格式化逻辑
        # - 设置百分比格式
        # - 设置日期格式
        # - 设置列宽
        # - 添加表头样式
        # - 冻结首行

        logger.info("报表格式化完成 ✓")
