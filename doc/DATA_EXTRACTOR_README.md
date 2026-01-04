# 数据抽取器使用说明

## 功能简介

数据抽取器用于从PostgreSQL数据库中自动抽取数据并生成3个Excel文件:
- **原始数据.xlsx** - 原始问题数据
- **计算数据.xlsx** - 计算后的数据
- **本周新增问题.xlsx** - 本周新增的问题列表

## 快速开始

### 1. 使用默认配置

```bash
python data_extractor.py
```

这将使用默认配置:
- Schema日期: 自动计算本周周一
- 筛选日期: 自动计算上周一至周日
- 输出目录: `output/`

### 2. 指定Schema日期

```bash
python data_extractor.py --schema-date 20251229
```

### 3. 指定筛选日期范围

```bash
python data_extractor.py --start-date 2025-12-22 --end-date 2025-12-28
```

### 4. 只执行特定任务

```bash
# 只执行任务1(原始数据)
python data_extractor.py --task1 1 --task2 0 --task3 0

# 只执行任务3(本周新增问题)
python data_extractor.py --task1 0 --task2 0 --task3 1
```

### 5. 指定输出目录

```bash
python data_extractor.py --output-dir custom_output/
```

## 配置文件

配置文件位于: `config/data_extractor.yaml`

### 数据库连接配置

```yaml
database:
  host: "172.16.215.119"
  port: 5432
  database: "postgres"
  user: "admin"
  password: "admin"
```

### Schema配置

```yaml
schema:
  date: null  # null表示自动计算本周周一,或指定如: 20251229
```

### 日期范围配置

```yaml
date_range:
  start_date: null  # null表示自动计算上周周一,或指定如: 2025-12-22
  end_date: null    # null表示自动计算上周周日,或指定如: 2025-12-28
```

### 输出配置

```yaml
output:
  directory: "output"
  files:
    task1: "原始数据.xlsx"
    task2: "计算数据.xlsx"
    task3: "本周新增问题.xlsx"
```

## 任务说明

### 任务1: 原始数据抽取

**数据源**: `yxwtzb_YYYYMMDD.导出原始数据`
**输出文件**: `原始数据.xlsx`
**筛选条件**: 无(导出全部数据)
**排序**: 按 `创建时间` 降序

### 任务2: 计算数据抽取

**数据源**: `yxwtzb_YYYYMMDD.计算解决率过程数据`
**输出文件**: `计算数据.xlsx`
**筛选条件**: 无(导出全部数据)
**排序**: 按 `创建时间` 降序

### 任务3: 本周新增问题抽取

**数据源**: `yxwtzb_YYYYMMDD.计算解决率过程数据`
**输出文件**: `本周新增问题.xlsx`
**筛选条件**:
- 创建时间在指定范围内(默认上周一至周日)
- 审批状态 ≠ '终止'
- 处理方式 NOT IN ('非研发处理', '硬件故障处理')
- 审批结果 ≠ '审批未通过'
**排序**: 按 `创建时间` 降序

**特殊字段**:
- "原因分析及解决方案": 固定文本 `'问题原因：xxx 解决方案：xxx (自行修改)'`
- "计划解决时间(最新计划)": 固定空值

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| --config | 配置文件路径 | --config custom.yaml |
| --schema-date | Schema日期(YYYYMMDD) | --schema-date 20251229 |
| --start-date | 起始日期(YYYY-MM-DD) | --start-date 2025-12-22 |
| --end-date | 结束日期(YYYY-MM-DD) | --end-date 2025-12-28 |
| --output-dir | 输出目录 | --output-dir output/ |
| --task1 | 是否执行任务1(0/1) | --task1 1 |
| --task2 | 是否执行任务2(0/1) | --task2 1 |
| --task3 | 是否执行任务3(0/1) | --task3 1 |

## 日志文件

日志文件保存在 `logs/` 目录:
- 文件名格式: `data_extractor_YYYYMMDD_HHMMSS.log`
- 日志级别: INFO
- 保留时间: 7天

## 日期计算逻辑

### Schema日期

**默认**: 使用本周周一
- 例如: 如果今天是2026-01-04(周日),本周周一是2025-12-29
- Schema名称: `yxwtzb_20251229`

**手动指定**: 使用 `--schema-date` 参数

### 筛选日期范围

**默认**: 使用上周一至周日
- 例如: 如果今天是2026-01-04(周日)
- 上周一: 2025-12-22
- 上周日: 2025-12-28
- 筛选范围: `2025-12-22 00:00:01` 至 `2025-12-28 23:59:59`

**手动指定**: 使用 `--start-date` 和 `--end-date` 参数

## 常见问题

### 1. 数据库连接失败

**错误信息**: `数据库连接失败`

**解决方法**:
- 检查配置文件中的数据库连接信息
- 确认数据库服务是否启动
- 检查网络连接

### 2. 表不存在

**错误信息**: `表不存在: yxwtzb_YYYYMMDD.表名`

**解决方法**:
- 确认Schema日期是否正确
- 检查数据库中是否存在该Schema和表
- 使用正确的Schema日期

### 3. 查询结果为空

**警告信息**: `查询结果为空`

**解决方法**:
- 检查筛选日期范围是否正确
- 确认该时间段内是否有数据
- 查看日志中的详细SQL语句

### 4. 字段缺失

**警告信息**: `字段缺失: 字段名`

**解决方法**:
- 确认源表结构是否完整
- 检查字段名是否正确(注意大小写)

## 性能指标

- **数据量**: 791行数据
- **处理时间**: < 5秒
- **内存占用**: < 50MB
- **输出文件**: 每个约200-300KB

## 开发者

如需修改或扩展功能,请参考以下文件:
- `src/data_extractor.py` - 数据抽取器
- `src/db_connector.py` - 数据库连接器
- `src/date_utils.py` - 日期工具
- `config/data_extractor.yaml` - 配置文件

## 测试

运行测试:
```bash
pytest tests/test_data_extractor.py -v
```

## 许可证

MIT License
