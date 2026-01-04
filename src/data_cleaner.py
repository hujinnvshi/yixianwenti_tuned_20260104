"""
数据清洗模块
负责数据筛选标记和清洗
"""

import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger


class DataCleaner:
    """数据清洗器"""

    def __init__(self, config: Dict):
        """
        初始化数据清洗器

        Args:
            config: 配置字典
        """
        self.config = config

    def mark_removal_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        标记需要剔除的行

        规则:
        1. 审批结果 = "审批未通过"
        2. 审批状态 = "终止"
        3. 非研发处理问题类别包含"需求"

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 标记后的数据框
        """
        logger.info("开始标记需要剔除的行...")

        # 初始化是否剔除列为NO(如果不存在)
        if '是否剔除' not in df.columns:
            df['是否剔除'] = 'NO'
            logger.info("创建'是否剔除'列,默认值为'NO'")

        initial_yes_count = (df['是否剔除'] == 'YES').sum()

        # 条件1: 审批结果 = "审批未通过"
        condition1 = df['审批结果'] == '审批未通过'
        count1 = condition1.sum()
        logger.info(f"条件1 - 审批结果='审批未通过': {count1}行")

        # 条件2: 审批状态 = "终止"
        condition2 = df['审批状态'] == '终止'
        count2 = condition2.sum()
        logger.info(f"条件2 - 审批状态='终止': {count2}行")

        # 条件3: 非研发处理问题类别包含"需求"
        condition3 = df['非研发处理问题类别'].str.contains('需求', na=False)
        count3 = condition3.sum()
        logger.info(f"条件3 - 非研发处理问题类别包含'需求': {count3}行")

        # 合并所有条件(OR关系)
        all_conditions = condition1 | condition2 | condition3
        df.loc[all_conditions, '是否剔除'] = 'YES'

        final_yes_count = (df['是否剔除'] == 'YES').sum()
        new_marked = final_yes_count - initial_yes_count

        logger.info(f"""
        数据筛选标记完成:
        - 新标记为YES的行数: {new_marked}
        - 总计YES的行数: {final_yes_count}
        - 总计NO的行数: {(df['是否剔除'] == 'NO').sum()}
        - 保留比例: {(df['是否剔除'] == 'NO').sum() / len(df) * 100:.2f}%
        """)

        return df

    def get_filtered_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        获取筛选后的数据(是否剔除=NO)

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 筛选后的数据框
        """
        filtered_df = df[df['是否剔除'] == 'NO'].copy()
        logger.info(f"获取筛选后数据: {len(filtered_df)}行 (原始: {len(df)}行)")
        return filtered_df

    def generate_removal_report(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        生成筛选报告

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 筛选报告
        """
        report = {
            '指标': ['总行数', '剔除行数', '保留行数', '保留比例'],
            '数值': [
                len(df),
                (df['是否剔除'] == 'YES').sum(),
                (df['是否剔除'] == 'NO').sum(),
                f"{(df['是否剔除'] == 'NO').sum() / len(df) * 100:.2f}%"
            ]
        }

        report_df = pd.DataFrame(report)
        return report_df
