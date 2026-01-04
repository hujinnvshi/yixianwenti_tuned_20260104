# 一线问题跟踪数据处理系统

## 项目简介

本系统用于处理一线问题跟踪数据,自动计算研发交付日期偏差、生成解决率透视表,并输出标准化的Excel报表。

## 功能特性

- ✅ 数据加载和质量检查
- ✅ 智能数据筛选和清洗
- ✅ 研发交付日期偏差计算(AE列)
- ✅ 解决状态分类统计(AO列)
- ✅ 数据副本列生成
- ✅ 透视表自动生成
- ✅ 解决率和及时解决率计算
- ✅ Excel报表格式化输出
- ✅ 完整的日志记录

## 技术栈

- Python 3.8+
- pandas: 数据处理
- openpyxl: Excel读写
- xlsxwriter: Excel格式化
- loguru: 日志管理
- pytest: 单元测试

## 项目结构

```
.
├── config/                 # 配置文件
│   └── config.yaml        # 主配置文件
├── data/                   # 数据目录
│   ├── 计算.xlsx          # 表格1
│   └── 原始.xlsx          # 表格2
├── src/                    # 源代码
│   ├── __init__.py
│   ├── data_loader.py     # 数据加载模块
│   ├── data_cleaner.py    # 数据清洗模块
│   ├── calculator.py      # 计算模块
│   ├── pivot_generator.py # 透视表生成模块
│   └── report_generator.py # 报表生成模块
├── tests/                  # 测试文件
│   ├── __init__.py
│   └── test_calculator.py # 计算模块测试
├── output/                 # 输出目录
├── logs/                   # 日志目录
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖列表
├── TODO.md                # 任务清单
└── README.md              # 本文件
```

## 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 快速开始

```bash
# 运行主程序
python main.py
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行测试并显示覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 配置说明

配置文件位于 `config/config.yaml`,主要配置项:

```yaml
input:
  table1: "data/计算.xlsx"      # 表格1路径
  table2: "data/原始.xlsx"      # 表格2路径
  sheet_name: "Result 1"        # Sheet名称

output:
  directory: "output"           # 输出目录
  filename: "第52周一线问题跟踪确认-20260104.xlsx"  # 输出文件名

logging:
  level: "INFO"                # 日志级别
  file: "logs/data_processing.log"  # 日志文件
```

## 输出说明

程序会生成包含3个Sheet的Excel文件:

1. **2025122911704000480**: 表格2原始数据备份
2. **计算解决率过程数据(调整后)**: 表格1处理后的完整数据
3. **计算解决率**: 透视表汇总结果

## 核心计算逻辑

### AE列: 研发交付日期偏差

计算实际解决时间与期望时间的偏差天数:
- 基准日期 = 计划完成时间(为空则用期望解决时间)
- 实际日期 = 研发解决时间(为空则用更新时间或当前时间)
- 天数偏差 = 实际日期 - 基准日期

### AO列: 用于交付日期偏差统计

根据天数偏差判断解决状态:
- 及时解决: 偏差 <= 0
- 未及时解决: 偏差 > 0 且已解决
- 超时未解决: 偏差 > 0 且未解决
- 处理中暂未超时: 偏差 <= 0 且未解决

## 日志

程序运行日志保存在 `logs/` 目录:
- `data_processing_YYYYMMDDHHMMSS.log`: 每次运行的详细日志

## 开发指南

### 添加新功能

1. 在 `src/` 目录创建新模块
2. 在 `main.py` 中集成
3. 在 `tests/` 添加对应测试
4. 更新 `TODO.md` 任务清单

### 代码风格

- 遵循 PEP 8 规范
- 使用类型注解
- 添加文档字符串
- 保持函数简洁

## 常见问题

### 1. 文件不存在错误

确保 `data/` 目录下有 `计算.xlsx` 和 `原始.xlsx` 文件。

### 2. 日期格式错误

检查Excel中的日期列格式是否正确。

### 3. 内存不足

数据量大时可以考虑分批处理。

## 性能指标

- 处理速度: ~791行/秒
- 内存占用: < 100MB
- 输出文件: ~200KB

## 维护者

- Your Name

## 许可证

MIT License

## 更新日志

### v1.0.0 (2026-01-04)
- ✨ 初始版本发布
- ✅ 完成核心功能实现
- ✅ 添加单元测试
- ✅ 完善文档
