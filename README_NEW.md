# 一线问题跟踪管理系统

## 项目简介

本项目包含两个独立的应用系统,用于一线问题跟踪管理:

1. **数据处理应用** - 处理Excel数据,计算解决率并生成报表
2. **数据抽取应用** - 从PostgreSQL数据库抽取数据并生成Excel文件

## 项目结构

```
yixianwenti_tuned_20260104/
├── apps/                           # 应用程序目录
│   ├── data_processor/             # 数据处理应用
│   │   ├── main.py                # 主程序入口
│   │   ├── config.yaml            # 配置文件
│   │   └── modules/               # 功能模块
│   │       ├── data_loader.py     # 数据加载
│   │       ├── data_cleaner.py    # 数据清洗
│   │       ├── calculator.py      # 计算(AE列/AO列)
│   │       ├── pivot_generator.py # 透视表生成
│   │       └── report_generator.py # 报表生成
│   │
│   └── data_extractor/             # 数据抽取应用
│       ├── main.py                # 主程序入口
│       ├── config.yaml            # 配置文件
│       └── modules/               # 功能模块
│           ├── date_utils.py      # 日期工具
│           ├── db_connector.py    # 数据库连接
│           └── extractor.py       # 数据抽取器
│
├── tests/                          # 测试目录
├── docs/                           # 文档目录
├── data/                           # 数据目录
├── output/                         # 输出目录
├── logs/                           # 日志目录
├── run_processor.sh               # 数据处理启动脚本
├── run_extractor.sh               # 数据抽取启动脚本
└── requirements.txt                # 依赖管理
```

## 快速开始

### 1. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 数据处理应用

```bash
# 使用启动脚本
./run_processor.sh

# 或直接运行
cd apps/data_processor
python3 main.py
```

### 3. 数据抽取应用

```bash
# 使用启动脚本
./run_extractor.sh

# 或直接运行
cd apps/data_extractor
python3 main.py
```

详细文档请查看项目文档。
