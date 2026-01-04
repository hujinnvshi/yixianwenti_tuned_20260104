"""
一线问题跟踪数据处理系统 - 主程序
"""

import sys
import yaml
from pathlib import Path
from loguru import logger
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from data_cleaner import DataCleaner
from calculator import Calculator
from pivot_generator import PivotGenerator
from report_generator import ReportGenerator


def load_config(config_path: str = 'config/config.yaml') -> dict:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        dict: 配置字典
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def main():
    """主函数"""

    # 配置日志
    logger.add(
        "logs/data_processing_{time}.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO"
    )

    logger.info("=" * 80)
    logger.info("一线问题跟踪数据处理系统 - 启动")
    logger.info("=" * 80)

    try:
        # 1. 加载配置
        logger.info("步骤1: 加载配置文件...")
        config = load_config()
        logger.info("配置文件加载成功 ✓")

        # 2. 加载数据
        logger.info("\n步骤2: 加载数据...")
        loader = DataLoader(config)
        df1, df2 = loader.load_all_data()
        logger.info("数据加载完成 ✓")

        # 3. 数据清洗
        logger.info("\n步骤3: 数据清洗...")
        cleaner = DataCleaner(config)
        df1 = cleaner.mark_removal_rows(df1)
        removal_report = cleaner.generate_removal_report(df1)
        logger.info("数据清洗完成 ✓")

        # 4. 计算AE列
        logger.info("\n步骤4: 计算AE列(研发交付日期偏差)...")
        calculator = Calculator(config)
        df1 = calculator.calculate_ae_column(df1)
        logger.info("AE列计算完成 ✓")

        # 5. 计算AO列
        logger.info("\n步骤5: 计算AO列(用于交付日期偏差统计)...")
        df1 = calculator.calculate_ao_column(df1)
        logger.info("AO列计算完成 ✓")

        # 6. 创建数据副本列
        logger.info("\n步骤6: 创建数据副本列...")
        df1 = calculator.create_data_copy_column(df1)
        logger.info("数据副本列创建完成 ✓")

        # 7. 创建透视表
        logger.info("\n步骤7: 创建透视表...")
        pivot_gen = PivotGenerator(config)
        pivot_table = pivot_gen.create_pivot_table(df1)
        pivot_with_metrics = pivot_gen.calculate_metrics(pivot_table)
        pivot_sorted = pivot_gen.sort_by_timely_rate(pivot_with_metrics)
        pivot_report = pivot_gen.generate_pivot_report(pivot_sorted)
        logger.info(f"透视表创建完成 ✓")
        logger.info(f"透视表报告: {pivot_report}")

        # 8. 生成报表
        logger.info("\n步骤8: 生成报表...")
        reporter = ReportGenerator(config)
        output_path = reporter.generate_report(df2, df1, pivot_sorted)
        logger.info("报表生成完成 ✓")

        # 9. 完成
        logger.info("\n" + "=" * 80)
        logger.info("数据处理完成!")
        logger.info(f"输出文件: {output_path}")
        logger.info(f"处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"处理过程中发生错误: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
