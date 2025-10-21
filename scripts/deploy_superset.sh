#!/bin/bash
# Superset部署脚本

echo "=== 部署Apache Superset仪表板 ==="

# 检查Superset是否已安装
if ! command -v superset &> /dev/null; then
    echo "安装Apache Superset..."
    pip install apache-superset
    superset db upgrade
    superset fab create-admin
    superset init
fi

# 启动Superset服务
echo "启动Superset服务..."
superset run -p 8088 --with-threads --reload --debugger &

# 等待服务启动
sleep 10

# 导入数据库连接配置
echo "配置数据库连接..."
python config/superset_config.py

# 创建仪表板
echo "创建RFM分析仪表板..."
superset import-dashboards -p config/superset_dashboard.json

echo "Superset部署完成！"
echo "访问地址: http://localhost:8088"
echo "默认用户名: admin"
echo "默认密码: admin"
