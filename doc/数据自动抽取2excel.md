# 数据自动抽取2excel
- 原始数据.xlsx
select * from yxwtzb_20251229.导出原始数据 A1 order by 创建时间 desc;
- 计算数据.xlsx
select * from yxwtzb_20251229.计算解决率过程数据 order by 创建时间 desc;
- 本周新增问题.xlsx
DROP TABLE IF EXISTS yxwtzb_20251229.本周新增问题;

-- 以后新增问题增加字段 "数据id"
CREATE TABLE IF NOT EXISTS yxwtzb_20251229.本周新增问题 (
    序号 SERIAL PRIMARY KEY,
    所属客户项目 VARCHAR(255),
    项目类型 VARCHAR(255),
    所涉产品 VARCHAR(255),
    软件版本号 VARCHAR(255),
    紧急程度 VARCHAR(255),
    问题描述 TEXT,
    原因分析及解决方案 TEXT,
    问题处理类别 VARCHAR(255),
    期望解决时间 VARCHAR(255),
    计划解决时间（系统导出） VARCHAR(255),
    计划解决时间（最新计划） VARCHAR(255),
    当前负责人 VARCHAR(255),
    研发负责人 VARCHAR(255),
    状态（以系统导出计算） VARCHAR(255),
    数据id VARCHAR(255),
    审批状态 VARCHAR(255),
    创建时间 VARCHAR(255)
);
truncate table yxwtzb_20251229.本周新增问题;
insert into yxwtzb_20251229.本周新增问题
SELECT "序号",
       "所属客户项目",
       "项目类型",
       "所涉产品",
       "软件版本号",
       "紧急程度",
       "问题描述",
       '问题原因：xxx 解决方案：xxx (自行修改)',
       "处理方式",
       "期望解决时间",
       "计划完成时间",
       '',
       "当前负责人",
       "研发负责人",
       "用于交付日期偏差统计",
       "数据id",
        审批状态,
        创建时间
FROM yxwtzb_20251229."计算解决率过程数据" A
where A.创建时间 >= '2025-12-29 00:00:01'
  AND A.创建时间 <= '2025-12-31 23:59:59'
  -- 注意：此处需要手动修改
  And A.审批状态 <> '终止' --手动剔除终止状态，和需求类.
  And (A.处理方式 not in ('非研发处理','硬件故障处理')  )
  And (A.审批结果 <> '审批未通过')
  -- And A."用于交付日期偏差统计" <> '及时解决'
order by 创建时间 desc;

-- 手动剔除终止状态，和需求类，注意问题分类需要明确。
select * from yxwtzb_20251229.本周新增问题 A order by A.创建时间 desc;
我想将这三个表的提取工作都放到一个python脚本中，实现自动抽取。
注意上面的yxwtzb_20251229是和日期相关的，需要根据实际日期进行修改。一般为本周周一对应的日期，但是特殊情况也可以手动修改。本周新增问题中的创建日期默认为上周的周一到周日，如有需要可以手动修改。
当前数据库是Postgresql，连接信息为：
pgsql164-172.16.215.119-5432-postgres-admin-admin