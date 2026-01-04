#!/usr/bin/env python3
"""
项目结构验证脚本
"""

import os
from pathlib import Path

def verify_structure():
    """验证项目结构"""
    
    print("=" * 80)
    print("项目结构验证")
    print("=" * 80)
    
    # 检查apps目录
    apps_dirs = [
        'apps/data_processor/modules',
        'apps/data_extractor/modules'
    ]
    
    for dir_path in apps_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path}")
            # 列出模块文件
            modules = list(Path(dir_path).glob('*.py'))
            for module in modules:
                if module.name != '__init__.py':
                    print(f"  - {module.name}")
        else:
            print(f"✗ {dir_path} (不存在)")
    
    print("\n" + "=" * 80)
    print("配置文件检查")
    print("=" * 80)
    
    config_files = [
        'apps/data_processor/config.yaml',
        'apps/data_extractor/config.yaml'
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✓ {config_file}")
        else:
            print(f"✗ {config_file} (不存在)")
    
    print("\n" + "=" * 80)
    print("主程序检查")
    print("=" * 80)
    
    main_files = [
        'apps/data_processor/main.py',
        'apps/data_extractor/main.py'
    ]
    
    for main_file in main_files:
        if Path(main_file).exists():
            print(f"✓ {main_file}")
        else:
            print(f"✗ {main_file} (不存在)")
    
    print("\n" + "=" * 80)
    print("启动脚本检查")
    print("=" * 80)
    
    scripts = [
        'run_processor.sh',
        'run_extractor.sh'
    ]
    
    for script in scripts:
        if Path(script).exists():
            is_executable = os.access(script, os.X_OK)
            status = "✓" if is_executable else "✗ (无执行权限)"
            print(f"{status} {script}")
        else:
            print(f"✗ {script} (不存在)")
    
    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80)

if __name__ == '__main__':
    verify_structure()
