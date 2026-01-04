#!/usr/bin/env python3
"""
数据抽取器 - 主程序
从PostgreSQL数据库抽取数据并生成Excel文件
"""

import sys
import argparse
import yaml
from pathlib import Path
from loguru import logger
from datetime import datetime

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_extractor import DataExtractor


def load_config(config_path: str = 'config/data_extractor.yaml') -> dict:
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


def setup_logging(config: dict):
    """配置日志系统"""
    log_config = config.get('logging', {})
    log_file = log_config.get('file', 'logs/data_extractor_{time}.log')
    log_level = log_config.get('level', 'INFO')

    logger.add(
        log_file.replace('{time}', datetime.now().strftime('%Y%m%d_%H%M%S')),
        rotation=log_config.get('rotation', '10 MB'),
        retention=log_config.get('retention', '7 days'),
        level=log_level
    )


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='从PostgreSQL数据库抽取数据并生成Excel文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用默认配置
  python data_extractor.py

  # 指定Schema日期
  python data_extractor.py --schema-date 20251229

  # 指定筛选日期范围
  python data_extractor.py --start-date 2025-12-22 --end-date 2025-12-28

  # 指定配置文件
  python data_extractor.py --config custom_config.yaml

  # 指定输出目录
  python data_extractor.py --output-dir output/
        """
    )

    parser.add_argument(
        '--config',
        default='config/data_extractor.yaml',
        help='配置文件路径 (默认: config/data_extractor.yaml)'
    )

    parser.add_argument(
        '--schema-date',
        help='Schema日期 (YYYYMMDD格式),例如: 20251229'
    )

    parser.add_argument(
        '--start-date',
        help='筛选起始日期 (YYYY-MM-DD格式),例如: 2025-12-22'
    )

    parser.add_argument(
        '--end-date',
        help='筛选结束日期 (YYYY-MM-DD格式),例如: 2025-12-28'
    )

    parser.add_argument(
        '--output-dir',
        help='输出目录路径,例如: output/'
    )

    parser.add_argument(
        '--task1',
        type=int,
        choices=[0, 1],
        help='是否执行任务1 (0=禁用, 1=启用)'
    )

    parser.add_argument(
        '--task2',
        type=int,
        choices=[0, 1],
        help='是否执行任务2 (0=禁用, 1=启用)'
    )

    parser.add_argument(
        '--task3',
        type=int,
        choices=[0, 1],
        help='是否执行任务3 (0=禁用, 1=启用)'
    )

    return parser.parse_args()


def override_config(config: dict, args) -> dict:
    """
    用命令行参数覆盖配置文件

    Args:
        config: 配置字典
        args: 命令行参数

    Returns:
        dict: 更新后的配置字典
    """
    if args.schema_date:
        config['schema']['date'] = args.schema_date
        logger.info(f"命令行覆盖: Schema日期 = {args.schema_date}")

    if args.start_date:
        config['date_range']['start_date'] = args.start_date
        logger.info(f"命令行覆盖: 起始日期 = {args.start_date}")

    if args.end_date:
        config['date_range']['end_date'] = args.end_date
        logger.info(f"命令行覆盖: 结束日期 = {args.end_date}")

    if args.output_dir:
        config['output']['directory'] = args.output_dir
        logger.info(f"命令行覆盖: 输出目录 = {args.output_dir}")

    if args.task1 is not None:
        config['tasks']['task1_enabled'] = bool(args.task1)
        logger.info(f"命令行覆盖: 任务1 = {'启用' if args.task1 else '禁用'}")

    if args.task2 is not None:
        config['tasks']['task2_enabled'] = bool(args.task2)
        logger.info(f"命令行覆盖: 任务2 = {'启用' if args.task2 else '禁用'}")

    if args.task3 is not None:
        config['tasks']['task3_enabled'] = bool(args.task3)
        logger.info(f"命令行覆盖: 任务3 = {'启用' if args.task3 else '禁用'}")

    return config


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_args()

    # 加载配置
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        logger.error(f"配置文件不存在: {args.config}")
        return 1
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return 1

    # 命令行参数覆盖配置
    config = override_config(config, args)

    # 配置日志
    setup_logging(config)

    logger.info("=" * 80)
    logger.info("数据抽取器启动")
    logger.info(f"配置文件: {args.config}")
    logger.info("=" * 80)

    try:
        # 创建数据抽取器
        extractor = DataExtractor(config)

        # 执行所有任务
        results = extractor.run_all_tasks()

        # 检查结果
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)

        if success_count == total_count:
            logger.info("✓ 所有任务执行成功")
            return 0
        else:
            logger.warning(f"部分任务失败: {success_count}/{total_count} 成功")
            return 1

    except Exception as e:
        logger.error(f"程序执行失败: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
