#!/bin/bash
# run_etl.sh - 自动化ETL流程 (最终修正版)
export HADOOP_HEAPSIZE=2048
export HIVE_HEAPSIZE=2048
unset HADOOP_CLIENT_OPTS

echo "【$(date)】ETL流程启动"

# 添加性能优化参数
OPTIONS="
--hiveconf hive.vectorized.execution.enabled=true
--hiveconf hive.vectorized.execution.reduce.enabled=true
--hiveconf hive.cbo.enable=true
--hiveconf hive.exec.parallel=true
"

# 步骤1：数据清洗
echo "执行数据清洗..."
hive $OPTIONS -f ~/video-behavior-analysis/sql_scripts/02_data_cleaning.hql

# 步骤2：维度加载
echo "加载维度表..."
hive $OPTIONS -f ~/video-behavior-analysis/sql_scripts/03_dimension_loading.hql

# 步骤3：事实表加载
echo "加载事实表..."
hive $OPTIONS -f ~/video-behavior-analysis/sql_scripts/04_fact_loading.hql

# 步骤4：执行分析
echo "生成分析结果..."
mkdir -p ~/video-behavior-analysis/results

# 执行并移动用户行为分析结果
hive $OPTIONS -f ~/video-behavior-analysis/sql_scripts/05_top_analysis.hql
mv /root/video-behavior-analysis/results/user_behavior_tmp/000000_0 /root/video-behavior-analysis/results/user_behavior.csv
mv /root/video-behavior-analysis/results/top_users_tmp/000000_0 /root/video-behavior-analysis/results/top_users.csv

# 执行并移动时段分析结果
hive $OPTIONS -f ~/video-behavior-analysis/sql_scripts/06_user_behavior.hql
mv /root/video-behavior-analysis/results/time_analysis_tmp/000000_0 /root/video-behavior-analysis/results/time_analysis.csv

# 创建带日期的副本
cp /root/video-behavior-analysis/results/user_behavior.csv /root/video-behavior-analysis/results/user_behavior_$(date +\%Y\%m\%d).csv
cp /root/video-behavior-analysis/results/top_users.csv /root/video-behavior-analysis/results/top_users_$(date +\%Y\%m\%d).csv
cp /root/video-behavior-analysis/results/time_analysis.csv /root/video-behavior-analysis/results/time_analysis_$(date +\%Y\%m\%d).csv

echo "【$(date)】ETL流程完成"
echo "结果文件:"
ls -l ~/video-behavior-analysis/results/*.csv

# 添加数据验证
echo -e "\n数据验证:"
hive -f ~/video-behavior-analysis/sql_scripts/validate.hql
# 在ETL流程最后添加可视化环节
echo "启动可视化流程..."
./run_visualizations.sh
