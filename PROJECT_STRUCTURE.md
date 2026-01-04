# 项目代码结构重组说明

## 📋 重组概述

将原有的两个独立功能模块分离,每个应用拥有独立的目录和配置,互不干扰。

## 🎯 重组目标

1. **模块分离** - 数据处理和数据抽取完全独立
2. **清晰结构** - 每个应用有独立的目录和模块
3. **便于维护** - 代码组织清晰,易于理解和修改
4. **独立运行** - 每个应用可以独立运行和部署

## 📁 新的项目结构

```
yixianwenti_tuned_20260104/
│
├── apps/                              # 应用程序目录(新增)
│   │
│   ├── data_processor/                # 数据处理应用
│   │   ├── __init__.py
│   │   ├── main.py                   # 主程序入口
│   │   ├── config.yaml               # 配置文件
│   │   └── modules/                  # 功能模块
│   │       ├── __init__.py
│   │       ├── data_loader.py        # 数据加载模块
│   │       ├── data_cleaner.py       # 数据清洗模块
│   │       ├── calculator.py         # 计算模块(AE/AO列)
│   │       ├── pivot_generator.py    # 透视表生成模块
│   │       └── report_generator.py   # 报表生成模块
│   │
│   └── data_extractor/                # 数据抽取应用
│       ├── __init__.py
│       ├── main.py                   # 主程序入口
│       ├── config.yaml               # 配置文件
│       └── modules/                  # 功能模块
│           ├── __init__.py
│           ├── date_utils.py         # 日期工具模块
│           ├── db_connector.py       # 数据库连接模块
│           └── extractor.py          # 数据抽取器模块
│
├── tests/                             # 测试目录(保持)
│   ├── __init__.py
│   ├── test_data_processor.py        # 数据处理测试
│   └── test_data_extractor.py        # 数据抽取测试
│
├── docs/                              # 文档目录
│   ├── yixianwenti_tuned.md          # 数据处理需求文档
│   └── 数据抽取需求文档.md            # 数据抽取需求文档
│
├── config/                            # 旧配置目录(可删除)
│   └── config.yaml
│
├── data/                              # 数据目录
│   ├── 计算.xlsx
│   └── 原始.xlsx
│
├── output/                            # 输出目录
├── logs/                              # 日志目录
│
├── venv/                              # 虚拟环境
│
├── src/                               # 旧源代码目录(可删除)
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── calculator.py
│   ├── pivot_generator.py
│   ├── report_generator.py
│   ├── date_utils.py
│   ├── db_connector.py
│   └── data_extractor.py
│
├── main.py                            # 旧主程序(可删除)
├── data_extractor.py                  # 旧主程序(可删除)
│
├── run_processor.sh                   # 数据处理启动脚本(新增)
├── run_extractor.sh                   # 数据抽取启动脚本(新增)
│
├── requirements.txt                   # 依赖管理
├── README.md                          # 项目说明
├── .gitignore
└── README_NEW.md                      # 新的项目说明
```

## 🔄 主要变更

### 1. 目录结构变更

| 旧路径 | 新路径 | 说明 |
|--------|--------|------|
| `main.py` | `apps/data_processor/main.py` | 数据处理主程序 |
| `data_extractor.py` | `apps/data_extractor/main.py` | 数据抽取主程序 |
| `src/data_loader.py` | `apps/data_processor/modules/data_loader.py` | 数据加载模块 |
| `src/calculator.py` | `apps/data_processor/modules/calculator.py` | 计算模块 |
| `src/pivot_generator.py` | `apps/data_processor/modules/pivot_generator.py` | 透视表模块 |
| `src/date_utils.py` | `apps/data_extractor/modules/date_utils.py` | 日期工具 |
| `src/db_connector.py` | `apps/data_extractor/modules/db_connector.py` | 数据库连接 |
| `src/data_extractor.py` | `apps/data_extractor/modules/extractor.py` | 数据抽取器 |
| `config/config.yaml` | `apps/data_processor/config.yaml` | 数据处理配置 |
| `config/data_extractor.yaml` | `apps/data_extractor/config.yaml` | 数据抽取配置 |

### 2. 配置文件变更

#### 数据处理配置
**位置**: `apps/data_processor/config.yaml`

```yaml
input:
  table1: "../../data/计算.xlsx"
  table2: "../../data/原始.xlsx"
  sheet_name: "Result 1"

output:
  directory: "../../output"
  filename: "第52周一线问题跟踪确认-20260104.xlsx"

logging:
  level: "INFO"
  file: "../../logs/data_processing_{time}.log"
```

**路径说明**: 使用相对路径 `../..` 因为从 `apps/data_processor/` 运行

#### 数据抽取配置
**位置**: `apps/data_extractor/config.yaml`

```yaml
database:
  host: "172.16.215.119"
  port: 5432
  database: "postgres"
  user: "admin"
  password: "admin"

schema:
  date: null

date_range:
  start_date: null
  end_date: null

output:
  directory: "../../output"
  files:
    task1: "原始数据.xlsx"
    task2: "计算数据.xlsx"
    task3: "本周新增问题.xlsx"

tasks:
  task1_enabled: true
  task2_enabled: true
  task3_enabled: true

logging:
  level: "INFO"
  file: "../../logs/data_extractor_{time}.log"
```

### 3. 启动脚本

#### 数据处理启动脚本
**文件**: `run_processor.sh`

```bash
#!/bin/bash
cd apps/data_processor
python3 main.py
```

#### 数据抽取启动脚本
**文件**: `run_extractor.sh`

```bash
#!/bin/bash
cd apps/data_extractor
python3 main.py "$@"
```

### 4. 运行方式变更

#### 旧方式(仍然兼容,但建议迁移)

```bash
# 旧的数据处理方式
python main.py

# 旧的数据抽取方式
python data_extractor.py --schema-date 20251229
```

#### 新方式(推荐)

```bash
# 新的数据处理方式
./run_processor.sh
# 或
cd apps/data_processor && python3 main.py

# 新的数据抽取方式
./run_extractor.sh --schema-date 20251229
# 或
cd apps/data_extractor && python3 main.py --schema-date 20251229
```

## ✅ 优势

### 1. 模块独立性
- 每个应用完全独立
- 互不依赖,可以单独部署
- 便于团队协作开发

### 2. 代码组织清晰
- 功能模块分类明确
- 易于查找和修改
- 降低维护成本

### 3. 扩展性更强
- 添加新应用只需创建新目录
- 模块可以方便地复用
- 便于微服务化改造

### 4. 部署灵活
- 可以独立打包部署
- 可以使用不同的配置
- 可以独立升级

## 📝 迁移指南

### 对于开发者

1. **更新工作流程**
   - 使用新的启动脚本
   - 配置文件移到各应用目录
   - 代码从 `apps/` 目录导入

2. **更新导入路径**
   ```python
   # 旧导入
   from data_loader import DataLoader

   # 新导入
   from apps.data_processor.modules.data_loader import DataLoader
   ```

3. **更新测试路径**
   ```python
   # 旧路径
   from src.calculator import Calculator

   # 新路径
   from apps.data_processor.modules.calculator import Calculator
   ```

### 对于用户

1. **使用新的启动脚本**
   - 数据处理: `./run_processor.sh`
   - 数据抽取: `./run_extractor.sh`

2. **配置文件位置变化**
   - 数据处理配置: `apps/data_processor/config.yaml`
   - 数据抽取配置: `apps/data_extractor/config.yaml`

3. **其他保持不变**
   - 输出目录: `output/`
   - 日志目录: `logs/`
   - 数据目录: `data/`

## 🗑️ 清理旧文件

迁移完成后,可以删除以下旧文件:

```bash
# 删除旧的源代码目录
rm -rf src/

# 删除旧的主程序
rm main.py
rm data_extractor.py

# 删除旧的配置目录
rm -rf config/

# 可选: 删除旧的文档和总结(已在新位置有更新版本)
rm PROJECT_SUMMARY.md
rm CHANGELOG.md
rm DATA_EXTRACTOR_README.md
rm DATA_EXTRACTOR_SUMMARY.md
```

**建议**: 先保留旧文件,测试新版本无问题后再删除。

## 🎊 总结

代码重组后,项目结构更加清晰:
- ✅ 两个应用完全独立
- ✅ 模块分类明确
- ✅ 配置文件独立
- ✅ 便于维护和扩展
- ✅ 保持向后兼容

可以开始使用新的项目结构了! 🚀
