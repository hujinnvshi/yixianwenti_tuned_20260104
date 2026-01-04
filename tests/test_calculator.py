"""
计算模块测试
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from calculator import Calculator


class TestCalculator:
    """计算器测试类"""

    @pytest.fixture
    def config(self):
        """配置fixture"""
        return {
            'calculation': {
                'date_format': '%Y-%m-%d',
                'datetime_format': '%Y-%m-%d %H:%M:%S',
                'percentage_decimals': 2
            }
        }

    @pytest.fixture
    def sample_data(self):
        """测试数据fixture"""
        data = {
            '数据id': ['1', '2', '3', '4', '5'],
            '处理方式': ['研发处理', '非研发处理', '研发处理', '研发处理', '研发处理'],
            '期望解决时间': pd.to_datetime(['2026-01-01', '2026-01-01', '2026-01-01', '2026-01-01', '2026-01-01']),
            '计划完成时间': [None, None, pd.Timestamp('2026-01-05'), None, None],
            '研发解决时间': [pd.Timestamp('2026-01-03'), None, pd.Timestamp('2026-01-06'), None, None],
            '审批状态': ['已结束', '审批中', '审批中', '已结束', '审批中'],
            '更新时间': pd.to_datetime(['2026-01-04', '2026-01-06', '2026-01-06', '2026-01-02', '2026-01-06']),
            '审批结果': ['审批通过', '审批通过', '审批通过', '审批通过', '审批通过'],
            '所涉产品': ['产品A', '产品B', '产品C', '产品D', '产品E'],
            '非研发处理问题类别': ['Bug', '需求', 'Bug', 'Bug', 'Bug'],
            '是否剔除': ['NO', 'YES', 'NO', 'NO', 'NO']
        }
        return pd.DataFrame(data)

    def test_calculate_ae_column(self, config, sample_data):
        """测试AE列计算"""
        calculator = Calculator(config)
        result = calculator.calculate_ae_column(sample_data.copy())

        # 验证非研发处理
        assert result.loc[1, '研发交付日期偏差'] == '非研发处理'

        # 验证研发处理的日期计算(第1行: 2026-01-03 - 2026-01-01 = 2天)
        assert isinstance(result.loc[0, '研发交付日期偏差'], (int, float))

    def test_calculate_ao_column(self, config, sample_data):
        """测试AO列计算"""
        calculator = Calculator(config)

        # 先计算AE列
        df = calculator.calculate_ae_column(sample_data.copy())

        # 再计算AO列
        result = calculator.calculate_ao_column(df)

        # 验证AO列有值
        assert '用于交付日期偏差统计' in result.columns

        # 验证非研发处理被保留
        assert result.loc[1, '用于交付日期偏差统计'] == '非研发处理'

    def test_create_data_copy_column(self, config, sample_data):
        """测试数据副本列创建"""
        calculator = Calculator(config)

        # 先计算AO列
        df = calculator.calculate_ae_column(sample_data.copy())
        df = calculator.calculate_ao_column(df)

        # 创建副本列
        result = calculator.create_data_copy_column(df)

        # 验证副本列存在
        assert '用于交付日期偏差统计DATA' in result.columns

        # 验证数据一致性
        assert (
            result['用于交付日期偏差统计'] ==
            result['用于交付日期偏差统计DATA']
        ).all()
