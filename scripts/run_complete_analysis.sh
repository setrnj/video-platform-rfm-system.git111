#!/bin/bash
# 完整分析流程执行脚本

echo "=== 视频平台RFM分析系统 - 完整分析流程 ==="

# 设置环境变量
export HADOOP_HEAPSIZE=2048
export HIVE_HEAPSIZE=2048
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 性能优化参数
OPTIONS="
--hiveconf hive.vectorized.execution.enabled=true
--hiveconf hive.vectorized.execution.reduce.enabled=true
--hiveconf hive.cbo.enable=true
--hiveconf hive.exec.parallel=true
"

# 步骤1: 数据生成（如果需要）
echo "【$(date)】步骤1: 数据生成"
if [ "$1" = "--generate-data" ]; then
    echo "生成模拟数据..."
    python src/data_generation/generate_simulated_data.py
    echo "数据生成完成"
fi

# 步骤2: ETL流程
echo "【$(date)】步骤2: 执行ETL流程"
echo "创建表结构..."
hive $OPTIONS -f sql_scripts/01_ddl_table_creation.hql

echo "数据清洗..."
hive $OPTIONS -f sql_scripts/02_data_cleaning.hql

echo "维度加载..."
hive $OPTIONS -f sql_scripts/03_dimension_loading.hql

echo "事实表加载..."
hive $OPTIONS -f sql_scripts/04_fact_loading.hql

# 步骤3: RFM分析
echo "【$(date)】步骤3: RFM分析"
echo "执行用户行为分析..."
hive $OPTIONS -f sql_scripts/05_top_analysis.hql

echo "执行时段分析..."
hive $OPTIONS -f sql_scripts/06_user_behavior.hql

echo "执行留存分析..."
hive $OPTIONS -f sql_scripts/07_user_retention.hql

# 步骤4: 数据聚类
echo "【$(date)】步骤4: 用户聚类分析"
python src/clustering/generate_segmentation.py

# 步骤5: 可视化生成
echo "【$(date)】步骤5: 生成可视化"
python src/visualization/generate_heatmap.py
python src/visualization/generate_charts.py
python src/clustering/generate_retention_curve.py

# 步骤6: 数据验证
echo "【$(date)】步骤6: 数据验证"
hive $OPTIONS -f sql_scripts/validate.hql

# 步骤7: 生成报告
echo "【$(date)】步骤7: 生成分析报告"
python src/visualization/generate_er_diagram.py

echo "【$(date)】完整分析流程完成！"
echo "结果文件位置:"
echo "  - 数据结果: data/results/"
echo "  - 图表输出: outputs/charts/"
echo "  - 分析报告: outputs/reports/"
echo "  - 系统日志: logs/"
