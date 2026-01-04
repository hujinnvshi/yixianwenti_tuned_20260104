"""
数据抽取应用测试
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加apps目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'apps' / 'data_extractor'))

from modules.date_utils import DateUtils


class TestDateUtils:
    """日期工具测试类"""

    def test_get_this_week_monday(self):
        """测试获取本周周一"""
        monday = DateUtils.get_this_week_monday()
        assert len(monday) == 8  # YYYYMMDD
        assert monday.isdigit()
        print(f"本周周一: {monday}")

    def test_get_last_week_range(self):
        """测试获取上周日期范围"""
        start_date, end_date = DateUtils.get_last_week_range()
        assert len(start_date) == 10  # YYYY-MM-DD
        assert len(end_date) == 10
        assert start_date <= end_date
        print(f"上周范围: {start_date} 至 {end_date}")

    def test_parse_schema_date(self):
        """测试解析Schema日期"""
        # YYYY-MM-DD格式
        result1 = DateUtils.parse_schema_date("2025-12-29")
        assert result1 == "20251229"

        # YYYYMMDD格式
        result2 = DateUtils.parse_schema_date("20251229")
        assert result2 == "20251229"

    def test_validate_date_range(self):
        """测试日期范围验证"""
        # 有效范围
        assert DateUtils.validate_date_range("2025-12-22", "2025-12-28") == True

        # 无效范围
        assert DateUtils.validate_date_range("2025-12-28", "2025-12-22") == False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
