#!/bin/bash

# 一线问题跟踪数据处理系统 - 启动脚本

echo "================================"
echo "一线问题跟踪数据处理系统"
echo "================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "虚拟环境不存在,正在创建..."
    python3 -m venv venv
    echo "虚拟环境创建完成"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "检查并安装依赖..."
pip install -q -r requirements.txt

# 创建必要的目录
mkdir -p output logs

# 运行程序
echo ""
echo "开始运行数据处理程序..."
echo ""
cd apps/data_processor
python3 main.py

# 检查运行结果
if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "程序运行成功!"
    echo "================================"
    echo ""
    echo "输出文件位置:"
    ls -lh ../../output/*.xlsx 2>/dev/null || echo "未找到输出文件"
    echo ""
    echo "日志文件位置:"
    ls -lht ../../logs/*.log 2>/dev/null | head -1 || echo "未找到日志文件"
else
    echo ""
    echo "================================"
    echo "程序运行失败,请查看日志"
    echo "================================"
    exit 1
fi
