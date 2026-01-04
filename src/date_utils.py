"""
日期工具模块
处理日期计算和格式化
"""

from datetime import datetime, timedelta, date
from typing import Tuple
from loguru import logger


class DateUtils:
    """日期工具类"""

    @staticmethod
    def get_this_week_monday() -> str:
        """
        获取本周周一的日期

        Returns:
            str: YYYYMMDD格式的日期字符串
        """
        today = datetime.now().date()
        # Monday is 0, Sunday is 6
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        return monday.strftime("%Y%m%d")

    @staticmethod
    def get_last_week_range() -> Tuple[str, str]:
        """
        获取上周的日期范围(周一到周日)

        Returns:
            Tuple[str, str]: (起始日期, 结束日期) 格式: YYYY-MM-DD
        """
        today = datetime.now().date()
        days_since_monday = today.weekday()
        this_monday = today - timedelta(days=days_since_monday)
        last_monday = this_monday - timedelta(weeks=1)
        last_sunday = last_monday + timedelta(days=6)

        start_date = last_monday.strftime("%Y-%m-%d")
        end_date = last_sunday.strftime("%Y-%m-%d")

        logger.info(f"上周日期范围: {start_date} 至 {end_date}")

        return start_date, end_date

    @staticmethod
    def parse_schema_date(date_str: str) -> str:
        """
        解析Schema日期

        Args:
            date_str: YYYYMMDD或YYYY-MM-DD格式的日期字符串

        Returns:
            str: YYYYMMDD格式的日期字符串
        """
        if '-' in date_str:
            # YYYY-MM-DD格式
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y%m%d")
        else:
            # YYYYMMDD格式
            return date_str

    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """
        格式化日期时间

        Args:
            dt: datetime对象

        Returns:
            str: YYYY-MM-DD HH:MM:SS格式的字符串
        """
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> bool:
        """
        验证日期范围是否有效

        Args:
            start_date: 起始日期 YYYY-MM-DD
            end_date: 结束日期 YYYY-MM-DD

        Returns:
            bool: 日期范围是否有效
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            is_valid = start <= end
            if not is_valid:
                logger.warning(f"日期范围无效: 起始日期 {start_date} 晚于结束日期 {end_date}")
            return is_valid
        except ValueError as e:
            logger.error(f"日期格式错误: {e}")
            return False
