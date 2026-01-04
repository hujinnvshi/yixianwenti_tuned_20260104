"""
数据抽取器模块
负责从数据库抽取数据并生成Excel文件
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from loguru import logger

from .db_connector import DatabaseConnector
from .date_utils import DateUtils


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

        # 生成文件名前缀
        self.date_prefix = self._get_date_prefix()

        # 初始化数据库连接
        self.db = DatabaseConnector(config)

    def _get_date_prefix(self) -> str:
        """
        获取文件名日期前缀

        Returns:
            str: 日期前缀,例如: "2026-01-04_"
        """
        if self.config['output'].get('date_prefix', False):
            prefix = datetime.now().strftime("%Y-%m-%d_")
            logger.info(f"使用日期前缀: {prefix}")
            return prefix
        else:
            logger.info("不使用日期前缀")
            return ""

    def _get_output_filename(self, filename_key: str) -> Path:
        """
        获取带前缀的输出文件名

        Args:
            filename_key: 配置文件中的键名(task1/task2/task3)

        Returns:
            Path: 完整的输出文件路径
        """
        base_filename = self.config['output']['files'][filename_key]
        filename = self.date_prefix + base_filename
        return self.output_dir / filename

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
            output_file = self._get_output_filename('task1')

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
            output_file = self._get_output_filename('task2')

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
            output_file = self._get_output_filename('task3')

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
                "用于交付日期偏差统计" AS "状态（以系统导出计算）"
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

            # 重新编号序号列
            if len(df) > 0 and '序号' in df.columns:
                df['序号'] = range(1, len(df) + 1)
                logger.info(f"序号已重新编号: 1 到 {len(df)}")

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

    def task4_extract_rdpm_data(self) -> bool:
        """
        任务4: RDPM导入数据抽取

        从数据库中抽取RDPM系统所需的导入数据

        Returns:
            bool: 执行是否成功
        """
        try:
            logger.info("=" * 80)
            logger.info("开始执行任务4: RDPM数据抽取")
            logger.info("=" * 80)

            # 获取输出文件名
            base_filename = self.config['output']['files']['task4']
            output_file = self._get_output_filename('task4')

            # SQL查询 - RDPM导入数据
            query = """
            SELECT
                A.创建时间,
                A.审批编号,
                A.所涉产品,
                A.软件版本号,
                A.所属客户项目,
                A.问题描述,
                B.部门负责人 as "测试负责人"
            FROM yxwtzb_"""+self.schema_date+""".计算解决率过程数据 A,
                 public."各产品对应的测试部长" B
            WHERE 1=1
              AND A.所涉产品=B."具体的产品"
              AND A.创建时间 >= %s
              AND A.创建时间 <= %s
              AND A.审批状态 <> %s
              AND A.审批结果 <> %s
              AND A.非研发处理问题类别 <> %s
            ORDER BY A.创建时间 DESC;
            """

            # 准备参数
            params = (
                f"{self.start_date} 00:00:01",
                f"{self.end_date} 23:59:59",
                '终止',
                '审批未通过',
                '需求'
            )

            # 执行查询
            df = self.db.execute_query(query, params=params)

            if len(df) == 0:
                logger.warning(f"查询结果为空,日期范围: {self.start_date} 至 {self.end_date}")
            else:
                logger.info(f"查询到 {len(df)} 条RDPM数据")

            # 重命名列为RDPM要求的格式
            rdpm_columns = {
                '创建时间': '一线问题提交时间(年-月-日 时：分：秒)(必填)',
                '审批编号': '审批编号(必填)',
                '所涉产品': '所涉产品(必填)',
                '软件版本号': '版本(必填)',
                '所属客户项目': '局点(必填)',
                '问题描述': '问题描述(必填)',
                '测试负责人': '测试负责人(必填)'
            }

            df = df.rename(columns=rdpm_columns)

            # 调整列顺序(按照RDPM要求的顺序)
            ordered_columns = [
                '一线问题提交时间(年-月-日 时：分：秒)(必填)',
                '审批编号(必填)',
                '所涉产品(必填)',
                '版本(必填)',
                '局点(必填)',
                '问题描述(必填)',
                '测试负责人(必填)'
            ]

            df = df[ordered_columns]

            # 写入Excel
            df.to_excel(output_file, sheet_name='RDPM导入数据', index=False)

            logger.info(f"""
            任务4完成 ✓
            - 输出文件: {output_file}
            - 数据行数: {len(df)}
            - 列数: {len(df.columns)}
            - 筛选范围: {self.start_date} 至 {self.end_date}
            - 表头格式: RDPM系统标准
            """)

            return True

        except Exception as e:
            logger.error(f"任务4执行失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
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
            if self.config['tasks'].get('task1_enabled', True):
                results['task1'] = self.task1_extract_original_data()

            # 执行任务2
            if self.config['tasks'].get('task2_enabled', True):
                results['task2'] = self.task2_extract_calculated_data()

            # 执行任务3
            if self.config['tasks'].get('task3_enabled', True):
                results['task3'] = self.task3_extract_new_issues()

            # 执行任务4
            if self.config['tasks'].get('task4_enabled', True):
                results['task4'] = self.task4_extract_rdpm_data()

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
