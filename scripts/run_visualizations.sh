#!/bin/bash

# 创建文档目录
mkdir -p docs

# 1. 执行SQL分析
echo "执行RFM和留存分析..."
hive -f sql_scripts/05_top_analysis.hql

echo "执行时段分析..."
hive -f sql_scripts/06_user_behavior.hql

# 2. 生成可视化文档
echo "生成用户分群报告..."
python scripts/generate_segmentation.py

echo "生成时段热力图..."
python scripts/generate_heatmap.py

echo "生成留存曲线..."
python scripts/generate_retention.py

echo "可视化文档生成完成! 查看docs目录:"
ls -lh docs/
