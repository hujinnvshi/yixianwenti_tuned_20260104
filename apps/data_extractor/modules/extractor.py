"""
数据抽取器模块
负责从数据库抽取数据并生成Excel文件
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from loguru import logger

from db_connector import DatabaseConnector
from date_utils import DateUtils


class DataExtractor:
    """数据抽取器"""

    def __init__(self, config: Dict):
        """
        初始化数据抽取器

        Args:
            config: 配置字典
        """
        self.config = config
        self.db_config = config['database']
        self.output_dir = Path(config['output']['directory'])
        self.schema_date = self._get_schema_date()
        self.start_date, self.end_date = self._get_date_range()

        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化数据库连接
        self.db = DatabaseConnector(config)

    def _get_schema_date(self) -> str:
        """
        获取Schema日期

        Returns:
            str: YYYYMMDD格式的日期
        """
        config_date = self.config['schema'].get('date')
        if config_date:
            logger.info(f"使用配置的Schema日期: {config_date}")
            return DateUtils.parse_schema_date(config_date)
        else:
            auto_date = DateUtils.get_this_week_monday()
            logger.info(f"自动计算的Schema日期(本周周一): {auto_date}")
            return auto_date

    def _get_date_range(self) -> tuple:
        """
        获取日期范围

        Returns:
            tuple: (start_date, end_date) 格式: YYYY-MM-DD
        """
        config_start = self.config['date_range'].get('start_date')
        config_end = self.config['date_range'].get('end_date')

        if config_start and config_end:
            logger.info(f"使用配置的日期范围: {config_start} 至 {config_end}")
            # 验证日期范围
            if DateUtils.validate_date_range(config_start, config_end):
                return config_start, config_end
            else:
                logger.warning("配置的日期范围无效,使用自动计算的范围")

        # 自动计算上周日期范围
        return DateUtils.get_last_week_range()

    def get_full_table_name(self, table_name: str) -> str:
        """
        获取完整的表名(包含Schema)

        Args:
            table_name: 表名

        Returns:
            str: schema.table_name格式
        """
        return f"yxwtzb_{self.schema_date}.\"{table_name}\""

    def task1_extract_original_data(self) -> bool:
        """
        任务1: 抽取原始数据

        Returns:
            bool: 是否成功
        """
        if not self.config['tasks'].get('task1_enabled', True):
            logger.info("任务1已禁用,跳过")
            return True

        logger.info("=" * 80)
        logger.info("开始执行任务1: 原始数据抽取")
        logger.info("=" * 80)

        try:
            table_name = self.get_full_table_name("导出原始数据")
            output_file = self.output_dir / self.config['output']['files']['task1']

            # 检查表是否存在
            if not self.db.table_exists(f"yxwtzb_{self.schema_date}", "导出原始数据"):
                logger.error(f"表不存在: {table_name}")
                return False

            # 构建SQL查询
            query = f"""
            SELECT *
            FROM {table_name}
            ORDER BY "创建时间" DESC;
            """

            # 执行查询
            df = self.db.execute_query(query)

            # 写入Excel
            df.to_excel(output_file, sheet_name='原始数据', index=False)

            logger.info(f"""
            任务1完成 ✓
            - 输出文件: {output_file}
            - 数据行数: {len(df)}
            - 列数: {len(df.columns)}
            """)

            return True

        except Exception as e:
            logger.error(f"任务1执行失败: {e}")
            return False

    def task2_extract_calculated_data(self) -> bool:
        """
        任务2: 抽取计算数据

        Returns:
            bool: 是否成功
        """
        if not self.config['tasks'].get('task2_enabled', True):
            logger.info("任务2已禁用,跳过")
            return True

        logger.info("=" * 80)
        logger.info("开始执行任务2: 计算数据抽取")
        logger.info("=" * 80)

        try:
            table_name = self.get_full_table_name("计算解决率过程数据")
            output_file = self.output_dir / self.config['output']['files']['task2']

            # 检查表是否存在
            if not self.db.table_exists(f"yxwtzb_{self.schema_date}", "计算解决率过程数据"):
                logger.error(f"表不存在: {table_name}")
                return False

            # 构建SQL查询
            query = f"""
            SELECT *
            FROM {table_name}
            ORDER BY "创建时间" DESC;
            """

            # 执行查询
            df = self.db.execute_query(query)

            # 写入Excel
            df.to_excel(output_file, sheet_name='计算解决率过程数据', index=False)

            logger.info(f"""
            任务2完成 ✓
            - 输出文件: {output_file}
            - 数据行数: {len(df)}
            - 列数: {len(df.columns)}
            """)

            return True

        except Exception as e:
            logger.error(f"任务2执行失败: {e}")
            return False

    def task3_extract_new_issues(self) -> bool:
        """
        任务3: 抽取本周新增问题

        Returns:
            bool: 是否成功
        """
        if not self.config['tasks'].get('task3_enabled', True):
            logger.info("任务3已禁用,跳过")
            return True

        logger.info("=" * 80)
        logger.info("开始执行任务3: 本周新增问题抽取")
        logger.info("=" * 80)

        try:
            table_name = self.get_full_table_name("计算解决率过程数据")
            output_file = self.output_dir / self.config['output']['files']['task3']

            # 检查表是否存在
            if not self.db.table_exists(f"yxwtzb_{self.schema_date}", "计算解决率过程数据"):
                logger.error(f"表不存在: {table_name}")
                return False

            # 构建SQL查询
            query = f"""
            SELECT
                "序号",
                "所属客户项目",
                "项目类型",
                "所涉产品",
                "软件版本号",
                "紧急程度",
                "问题描述",
                %s AS "原因分析及解决方案",
                "处理方式" AS "问题处理类别",
                "期望解决时间",
                "计划完成时间" AS "计划解决时间（系统导出）",
                %s AS "计划解决时间（最新计划）",
                "当前负责人",
                "研发负责人",
                "用于交付日期偏差统计" AS "状态（以系统导出计算）",
                "数据id",
                "审批状态",
                "创建时间"
            FROM {table_name}
            WHERE "创建时间" >= %s
              AND "创建时间" <= %s
              AND "审批状态" <> %s
              AND "处理方式" NOT IN (%s, %s)
              AND "审批结果" <> %s
            ORDER BY "创建时间" DESC;
            """

            params = (
                '问题原因：xxx 解决方案：xxx (自行修改)',  # 固定文本
                '',  # 空字符串
                f"{self.start_date} 00:00:01",
                f"{self.end_date} 23:59:59",
                '终止',
                '非研发处理',
                '硬件故障处理',
                '审批未通过'
            )

            # 执行查询
            df = self.db.execute_query(query, params=params)

            if len(df) == 0:
                logger.warning(f"查询结果为空,日期范围: {self.start_date} 至 {self.end_date}")
            else:
                logger.info(f"查询到 {len(df)} 条新增问题")

            # 写入Excel
            df.to_excel(output_file, sheet_name='本周新增问题', index=False)

            logger.info(f"""
            任务3完成 ✓
            - 输出文件: {output_file}
            - 数据行数: {len(df)}
            - 列数: {len(df.columns)}
            - 筛选范围: {self.start_date} 至 {self.end_date}
            """)

            return True

        except Exception as e:
            logger.error(f"任务3执行失败: {e}")
            return False

    def run_all_tasks(self) -> Dict[str, bool]:
        """
        运行所有抽取任务

        Returns:
            Dict[str, bool]: 各任务的执行结果
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("数据抽取任务开始")
        logger.info(f"Schema日期: {self.schema_date}")
        logger.info(f"筛选范围: {self.start_date} 至 {self.end_date}")
        logger.info("=" * 80)

        results = {}

        try:
            # 连接数据库
            self.db.connect()

            # 执行任务1
            results['task1'] = self.task1_extract_original_data()

            # 执行任务2
            results['task2'] = self.task2_extract_calculated_data()

            # 执行任务3
            results['task3'] = self.task3_extract_new_issues()

            # 断开数据库连接
            self.db.disconnect()

        except Exception as e:
            logger.error(f"数据抽取过程发生错误: {e}")
            self.db.disconnect()
            raise

        # 统计结果
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)

        logger.info("=" * 80)
        logger.info("数据抽取任务完成")
        logger.info(f"成功: {success_count}/{total_count}")
        logger.info(f"耗时: {duration:.2f}秒")
        logger.info("=" * 80)

        return results
