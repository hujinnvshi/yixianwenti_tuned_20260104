"""
数据加载模块
负责读取Excel数据并进行初步的数据质量检查
"""

import pandas as pd
from pathlib import Path
from typing import Tuple, Dict
from loguru import logger


class DataLoader:
    """数据加载器"""

    def __init__(self, config: Dict):
        """
        初始化数据加载器

        Args:
            config: 配置字典
        """
        self.config = config
        self.table1_path = Path(config['input']['table1'])
        self.table2_path = Path(config['input']['table2'])
        self.sheet_name1 = config['input'].get('sheet_name1', 'Result 1')
        self.sheet_name2 = config['input'].get('sheet_name2', 'Result 1')

    def load_table1(self) -> pd.DataFrame:
        """
        加载表格1(计算.xlsx)

        Returns:
            pd.DataFrame: 表格1的数据
        """
        logger.info(f"开始加载表格1: {self.table1_path}")

        if not self.table1_path.exists():
            raise FileNotFoundError(f"文件不存在: {self.table1_path}")

        df = pd.read_excel(self.table1_path, sheet_name=self.sheet_name1)

        logger.info(f"表格1加载成功: {len(df)}行 × {len(df.columns)}列")

        # 数据质量检查
        self._check_data_quality(df, "表格1")

        return df

    def load_table2(self) -> pd.DataFrame:
        """
        加载表格2(原始.xlsx)

        Returns:
            pd.DataFrame: 表格2的数据
        """
        logger.info(f"开始加载表格2: {self.table2_path}")

        if not self.table2_path.exists():
            raise FileNotFoundError(f"文件不存在: {self.table2_path}")

        df = pd.read_excel(self.table2_path, sheet_name=self.sheet_name2)

        logger.info(f"表格2加载成功: {len(df)}行 × {len(df.columns)}列")

        # 数据质量检查
        self._check_data_quality(df, "表格2")

        return df

    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        加载所有数据

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: (表格1, 表格2)
        """
        df1 = self.load_table1()
        df2 = self.load_table2()
        return df1, df2

    def _check_data_quality(self, df: pd.DataFrame, table_name: str):
        """
        检查数据质量

        Args:
            df: 数据框
            table_name: 表格名称
        """
        logger.info(f"开始检查{table_name}的数据质量...")

        # 基本统计
        total_rows = len(df)
        total_cols = len(df.columns)
        total_cells = total_rows * total_cols
        missing_cells = df.isnull().sum().sum()
        missing_percentage = (missing_cells / total_cells) * 100

        logger.info(f"""
        数据质量报告 - {table_name}:
        - 总行数: {total_rows}
        - 总列数: {total_cols}
        - 总单元格数: {total_cells}
        - 空值单元格数: {missing_cells}
        - 空值占比: {missing_percentage:.2f}%
        """)

        # 检查关键列是否存在
        required_columns = [
            '数据id', '处理方式', '期望解决时间', '计划完成时间',
            '研发解决时间', '审批状态', '审批结果', '更新时间',
            '所涉产品', '非研发处理问题类别', '是否剔除'
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.warning(f"警告: 以下关键列不存在: {missing_columns}")
        else:
            logger.info("所有关键列都存在 ✓")

        # 检查重复行
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            logger.warning(f"警告: 发现 {duplicate_rows} 行重复数据")
        else:
            logger.info("没有重复行 ✓")

        # 数据类型检查
        logger.info("数据类型信息:")
        for col in ['期望解决时间', '计划完成时间', '研发解决时间', '更新时间']:
            if col in df.columns:
                dtype = df[col].dtype
                logger.info(f"  - {col}: {dtype}")

        logger.info(f"{table_name}数据质量检查完成 ✓")
