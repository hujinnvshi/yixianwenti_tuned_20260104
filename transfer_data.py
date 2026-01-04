#!/usr/bin/env python3
"""
数据流转脚本
将数据抽取模块生成的数据拷贝到数据处理模块的data目录
"""

import shutil
from pathlib import Path
from datetime import datetime
from loguru import logger
import sys


def get_latest_files(source_dir: Path, pattern: str) -> Path:
    """
    获取最新的匹配文件

    Args:
        source_dir: 源目录
        pattern: 文件匹配模式

    Returns:
        Path: 最新文件的路径
    """
    files = list(source_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"未找到匹配的文件: {pattern}")

    # 按修改时间排序,返回最新的
    latest = max(files, key=lambda f: f.stat().st_mtime)
    return latest


def copy_data_files():
    """拷贝数据文件"""

    logger.add("../../logs/data_transfer_{time}.log", rotation="10 MB", retention="7 days")

    logger.info("=" * 80)
    logger.info("数据流转开始")
    logger.info("=" * 80)

    # 目录定义
    source_dir = Path("apps/data_extractor/output")
    target_dir = Path("data")

    # 确保目标目录存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 清空目标目录中的Excel文件
    logger.info("清空目标目录中的旧Excel文件...")
    old_files = list(target_dir.glob("*.xlsx"))
    for old_file in old_files:
        old_file.unlink()
        logger.info(f"  删除: {old_file.name}")

    # 查找最新生成的数据文件
    logger.info("\n查找最新生成的数据文件...")

    try:
        file_mapping = {
            '原始.xlsx': get_latest_files(source_dir, "*_原始数据.xlsx"),
            '计算.xlsx': get_latest_files(source_dir, "*_计算数据.xlsx")
        }

        logger.info(f"找到最新文件:")
        for target_name, source_file in file_mapping.items():
            logger.info(f"  {source_file.name}")

        # 拷贝文件并重命名
        logger.info("\n开始拷贝文件...")

        for target_name, source_file in file_mapping.items():
            target_file = target_dir / target_name

            shutil.copy2(source_file, target_file)

            # 显示文件信息
            size_kb = source_file.stat().st_size / 1024
            logger.info(f"  ✓ {source_file.name} -> {target_name} ({size_kb:.1f}KB)")

        logger.info("\n" + "=" * 80)
        logger.info("数据流转完成 ✓")
        logger.info(f"目标目录: {target_dir.absolute()}")
        logger.info("=" * 80)

        return True

    except Exception as e:
        logger.error(f"数据流转失败: {e}")
        return False


if __name__ == '__main__':
    success = copy_data_files()
    sys.exit(0 if success else 1)
