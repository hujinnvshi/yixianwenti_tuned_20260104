"""
透视表生成模块
负责创建透视表和计算字段
"""

import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger


class PivotGenerator:
    """透视表生成器"""

    def __init__(self, config: Dict):
        """
        初始化透视表生成器

        Args:
            config: 配置字典
        """
        self.config = config
        self.decimals = config['calculation']['percentage_decimals']

    def create_pivot_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建透视表

        筛选条件:
        - 是否剔除 = "NO"
        - 处理方式 in ["研发处理", "非研发处理"]

        透视表结构:
        - 行: 所涉产品
        - 列: 用于交付日期偏差统计
        - 值: count(数据id)

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 透视表
        """
        logger.info("开始创建透视表...")

        # 筛选数据
        filtered_df = df[
            (df['是否剔除'] == 'NO') &
            (df['处理方式'].isin(['研发处理', '非研发处理']))
        ].copy()

        logger.info(f"筛选后数据: {len(filtered_df)}行 (原始: {len(df)}行)")

        # 创建透视表
        pivot = pd.pivot_table(
            filtered_df,
            values='数据id',
            index='所涉产品',
            columns='用于交付日期偏差统计',
            aggfunc='count',
            fill_value=0
        )

        logger.info(f"透视表创建成功: {len(pivot)}个产品")

        return pivot

    def calculate_metrics(self, pivot: pd.DataFrame) -> pd.DataFrame:
        """
        计算解决率和及时解决率

        解决率 = (及时解决 + 未及时解决) / (总计 - 非研发 - 其他排除)
        及时解决率 = 及时解决 / (总计 - 非研发 - 其他排除)

        Args:
            pivot: 透视表

        Returns:
            pd.DataFrame: 添加计算字段的透视表
        """
        logger.info("开始计算解决率和及时解决率...")

        # 创建结果DataFrame
        result_df = pivot.copy()

        # 获取所有列名
        all_columns = pivot.columns.tolist()

        # 计算每个产品的统计指标
        for product in pivot.index:
            row_data = pivot.loc[product]

            # 各状态数量
            timely = row_data.get('及时解决', 0)
            not_timely = row_data.get('未及时解决', 0)
            timeout = row_data.get('超时未解决', 0)
            processing = row_data.get('处理中暂未超时', 0)
            non_dev = row_data.get('非研发处理', 0)

            # 计算总数
            total = row_data.sum()

            # 计算分母(总计 - 非研发 - 其他排除)
            # 这里"其他排除"指的是非正常流程的状态
            denominator = total - non_dev

            if denominator > 0:
                # 解决率
                resolution_rate = ((timely + not_timely) / denominator) * 100
                result_df.loc[product, '解决率'] = round(resolution_rate, self.decimals)

                # 及时解决率
                timely_rate = (timely / denominator) * 100
                result_df.loc[product, '及时解决率'] = round(timely_rate, self.decimals)
            else:
                result_df.loc[product, '解决率'] = '不涉及研发处理'
                result_df.loc[product, '及时解决率'] = '不涉及研发处理'

        logger.info("解决率和及时解决率计算完成 ✓")

        return result_df

    def sort_by_timely_rate(self, pivot_df: pd.DataFrame) -> pd.DataFrame:
        """
        按及时解决率从低到高排序

        Args:
            pivot_df: 透视表DataFrame

        Returns:
            pd.DataFrame: 排序后的透视表
        """
        logger.info("按及时解决率从低到高排序...")

        # 将及时解决率转换为数值(非数值的设为-1,排在最后)
        def convert_to_numeric(value):
            if isinstance(value, str):
                return -1
            return value

        pivot_df['_sort_key'] = pivot_df['及时解决率'].apply(convert_to_numeric)
        pivot_df = pivot_df.sort_values('_sort_key', ascending=True)
        pivot_df = pivot_df.drop('_sort_key', axis=1)

        logger.info("排序完成 ✓")

        return pivot_df

    def generate_pivot_report(self, pivot_df: pd.DataFrame) -> Dict:
        """
        生成透视表报告

        Args:
            pivot_df: 透视表DataFrame

        Returns:
            Dict: 报告字典
        """
        report = {
            '产品数量': len(pivot_df),
            '平均及时解决率': 'N/A',
            '最低及时解决率': 'N/A',
            '最高及时解决率': 'N/A'
        }

        # 提取数值型的及时解决率
        timely_rates = pivot_df['及时解决率'][
            pivot_df['及时解决率'].apply(lambda x: isinstance(x, (int, float)))
        ]

        if len(timely_rates) > 0:
            report['平均及时解决率'] = f"{timely_rates.mean():.2f}%"
            report['最低及时解决率'] = f"{timely_rates.min():.2f}%"
            report['最高及时解决率'] = f"{timely_rates.max():.2f}%"

        return report
