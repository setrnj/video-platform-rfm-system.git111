#!/bin/bash
# 环境初始化脚本

echo "=== 视频平台RFM分析系统环境初始化 ==="

# 设置环境变量
export HADOOP_HEAPSIZE=2048
export HIVE_HEAPSIZE=2048
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 创建HDFS目录结构
echo "创建HDFS目录结构..."
hadoop fs -mkdir -p /data/video_analysis/{raw/{media,users},cleaned,dwh,results}
hadoop fs -mkdir -p /results/{user_rfm,time_heatmap,retention_curve}

# 设置HDFS权限
hadoop fs -chmod -R 755 /data/video_analysis
hadoop fs -chmod -R 755 /results

# 初始化Hive数据库
echo "初始化Hive数据库..."
hive -e "CREATE DATABASE IF NOT EXISTS video_analysis;"
hive -e "USE video_analysis;"

# 创建Python虚拟环境
echo "创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install -r config/requirements.txt

# 创建日志目录
mkdir -p logs
mkdir -p outputs/{charts,reports}

echo "环境初始化完成！"
echo "请运行以下命令启动系统："
echo "  ./scripts/run_complete_analysis.sh"
