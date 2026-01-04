"""
计算模块
负责AE列和AO列的计算
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Union
from loguru import logger


class Calculator:
    """计算器"""

    def __init__(self, config: Dict):
        """
        初始化计算器

        Args:
            config: 配置字典
        """
        self.config = config
        self.date_format = config['calculation']['date_format']
        self.datetime_format = config['calculation']['datetime_format']

    def calculate_ae_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算AE列: 研发交付日期偏差

        业务逻辑:
        1. 判断基准日期: 计划完成时间(为空则用期望解决时间)
        2. 判断处理方式: 非研发处理返回"非研发处理"
        3. 计算实际完成日期: 研发解决时间(为空则用更新时间或当前时间)
        4. 计算天数偏差: 实际完成日期 - 基准日期

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 添加AE列的数据框
        """
        logger.info("开始计算AE列(研发交付日期偏差)...")

        # 创建AE列(如果不存在)
        if '研发交付日期偏差' not in df.columns:
            df['研发交付日期偏差'] = None
            logger.info("创建'研发交付日期偏差'列")

        # 确保日期列是datetime类型
        date_columns = ['期望解决时间', '计划完成时间', '研发解决时间', '更新时间']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # 逐行计算
        for idx in df.index:
            row = df.loc[idx]

            # 步骤1: 判断基准日期
            if pd.isna(row['计划完成时间']) or row['计划完成时间'] == '':
                baseline_date = row['期望解决时间']
            else:
                baseline_date = row['计划完成时间']

            # 步骤2: 判断处理方式
            if row['处理方式'] != '研发处理':
                df.loc[idx, '研发交付日期偏差'] = '非研发处理'
                continue

            # 如果基准日期为空,返回空值
            if pd.isna(baseline_date):
                df.loc[idx, '研发交付日期偏差'] = None
                continue

            # 步骤3: 计算实际完成日期
            if not pd.isna(row['研发解决时间']) and row['研发解决时间'] != '':
                actual_date = row['研发解决时间']
            else:
                # 研发解决时间为空
                if row['审批状态'] == '已结束':
                    actual_date = row['更新时间']
                else:
                    actual_date = datetime.now()

            # 步骤4: 计算天数偏差
            if not pd.isna(actual_date):
                days_diff = (actual_date - baseline_date).days
                df.loc[idx, '研发交付日期偏差'] = int(days_diff)
            else:
                df.loc[idx, '研发交付日期偏差'] = None

        # 统计结果
        non_dev_count = (df['研发交付日期偏差'] == '非研发处理').sum()
        numeric_count = df['研发交付日期偏差'].apply(lambda x: isinstance(x, (int, float))).sum()
        null_count = df['研发交付日期偏差'].isna().sum()

        logger.info(f"""
        AE列计算完成:
        - 非研发处理: {non_dev_count}行
        - 数值结果: {numeric_count}行
        - 空值: {null_count}行
        """)

        return df

    def calculate_ao_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算AO列: 用于交付日期偏差统计

        业务逻辑:
        1. 判断AE列是否为数字
        2. 判断是否已解决(研发解决时间不为空)
        3. 根据天数偏差判断状态

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 添加AO列的数据框
        """
        logger.info("开始计算AO列(用于交付日期偏差统计)...")

        # 创建AO列(如果不存在)
        if '用于交付日期偏差统计' not in df.columns:
            df['用于交付日期偏差统计'] = None
            logger.info("创建'用于交付日期偏差统计'列")

        # 确保研发解决时间是datetime类型
        if '研发解决时间' in df.columns:
            df['研发解决时间'] = pd.to_datetime(df['研发解决时间'], errors='coerce')

        # 逐行计算
        for idx in df.index:
            row = df.loc[idx]
            ae_value = row['研发交付日期偏差']

            # 步骤1: 判断AE列是否为数字
            if not isinstance(ae_value, (int, float)):
                df.loc[idx, '用于交付日期偏差统计'] = ae_value
                continue

            # 步骤2: 判断是否已解决
            if not pd.isna(row['研发解决时间']) and row['研发解决时间'] != '':
                # 已解决
                if ae_value > 0:
                    df.loc[idx, '用于交付日期偏差统计'] = '未及时解决'
                else:
                    df.loc[idx, '用于交付日期偏差统计'] = '及时解决'
            else:
                # 未解决
                if row['审批状态'] == '已结束':
                    if ae_value > 0:
                        df.loc[idx, '用于交付日期偏差统计'] = '未及时解决'
                    else:
                        df.loc[idx, '用于交付日期偏差统计'] = '及时解决'
                else:
                    if ae_value > 0:
                        df.loc[idx, '用于交付日期偏差统计'] = '超时未解决'
                    else:
                        df.loc[idx, '用于交付日期偏差统计'] = '处理中暂未超时'

        # 统计结果
        status_counts = df['用于交付日期偏差统计'].value_counts()
        logger.info(f"""
        AO列计算完成:
        {status_counts.to_string()}
        """)

        return df

    def create_data_copy_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建数据副本列: 用于交付日期偏差统计DATA

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 添加副本列的数据框
        """
        logger.info("开始创建数据副本列...")

        # 复制AO列到新列
        df['用于交付日期偏差统计DATA'] = df['用于交付日期偏差统计'].copy()

        # 验证数据一致性
        is_consistent = (
            df['用于交付日期偏差统计'] == df['用于交付日期偏差统计DATA']
        ).all()

        if is_consistent:
            logger.info("数据副本列创建成功 ✓ (数据完全一致)")
        else:
            logger.warning("警告: 数据副本列与原列不一致!")

        return df
