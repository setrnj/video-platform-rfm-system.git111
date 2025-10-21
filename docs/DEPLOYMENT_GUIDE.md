# 视频平台RFM分析系统部署指南

## 系统概述

本系统是一个完整的视频平台用户行为分析解决方案，基于Hadoop生态系统构建，实现了从数据采集到可视化分析的全流程自动化。

## 环境要求

### 硬件要求
- **CPU**: 8核心以上
- **内存**: 16GB以上
- **存储**: 100GB以上可用空间
- **网络**: 千兆以太网

### 软件要求
- **操作系统**: CentOS 7.x / Ubuntu 18.04+
- **Java**: JDK 8+
- **Hadoop**: 3.2.0+
- **Hive**: 3.1.2+
- **Python**: 3.6+
- **MySQL**: 5.7+ (用于Superset元数据存储)

## 部署步骤

### 1. 环境准备

```bash
# 创建项目目录
mkdir -p /opt/video-platform-rfm-system
cd /opt/video-platform-rfm-system

# 复制项目文件
cp -r /path/to/video-platform-rfm-system/* .

# 设置权限
chmod +x scripts/*.sh
```

### 2. 系统初始化

```bash
# 运行环境初始化脚本
bash scripts/setup_environment.sh
```

该脚本将自动完成：
- 创建HDFS目录结构
- 初始化Hive数据库
- 安装Python依赖
- 设置环境变量

### 3. 数据库配置

#### 3.1 Hive配置
```bash
# 编辑Hive配置文件
vim $HIVE_HOME/conf/hive-site.xml

# 添加以下配置
<property>
    <name>hive.exec.dynamic.partition</name>
    <value>true</value>
</property>
<property>
    <name>hive.exec.dynamic.partition.mode</name>
    <value>nonstrict</value>
</property>
```

#### 3.2 数据库连接配置
```bash
# 编辑数据库配置文件
vim config/database_config.yaml

# 根据实际环境修改连接参数
database:
  hive:
    host: "your-hive-host"
    port: 10000
    database: "video_analysis"
```

### 4. 数据准备

#### 4.1 上传原始数据
```bash
# 上传媒体数据
hadoop fs -put data/raw/media_sample.csv /data/video_analysis/raw/media/

# 上传用户数据
hadoop fs -put data/raw/user_sample.csv /data/video_analysis/raw/users/
```

#### 4.2 生成模拟数据（可选）
```bash
# 生成模拟数据
python main.py --generate-data
```

### 5. 执行分析流程

#### 5.1 完整分析流程
```bash
# 执行完整分析
python main.py --mode all
```

#### 5.2 分步执行
```bash
# 仅ETL流程
python main.py --mode etl

# 仅RFM分析
python main.py --mode rfm

# 仅可视化
python main.py --mode viz
```

### 6. Superset部署（可选）

#### 6.1 安装Superset
```bash
# 安装Superset
pip install apache-superset

# 初始化数据库
superset db upgrade
superset fab create-admin
superset init
```

#### 6.2 启动Superset
```bash
# 启动服务
bash scripts/deploy_superset.sh

# 访问地址: http://localhost:8088
```

## 配置说明

### 1. RFM分析配置 (`config/rfm_config.yaml`)

```yaml
rfm_analysis:
  scoring:
    recency_days: 30      # 最近活跃天数阈值
    frequency_threshold: 5 # 频次阈值
    monetary_threshold: 1000 # 金额阈值（分钟）
```

### 2. ETL配置 (`config/etl_config.yaml`)

```yaml
etl:
  performance:
    hive_vectorized: true
    hive_parallel: true
    memory_allocation: "2048m"
```

### 3. 可视化配置 (`config/visualization_config.yaml`)

```yaml
visualization:
  style:
    figure_size: [12, 8]
    dpi: 300
    color_palette: "viridis"
```

## 监控和维护

### 1. 日志监控
```bash
# 查看ETL日志
tail -f logs/etl.log

# 查看系统日志
tail -f logs/system.log
```

### 2. 性能监控
```bash
# 检查HDFS使用情况
hadoop fs -du -h /data/video_analysis

# 检查Hive表状态
hive -e "SHOW TABLES;"
```

### 3. 数据验证
```bash
# 执行数据验证
hive -f sql_scripts/validate.hql
```

## 故障排除

### 1. 常见问题

#### 问题1: Hive连接失败
```bash
# 检查Hive服务状态
jps | grep RunJar

# 重启Hive服务
hive --service metastore &
hive --service hiveserver2 &
```

#### 问题2: Python依赖问题
```bash
# 重新安装依赖
pip install -r config/requirements.txt --force-reinstall
```

#### 问题3: 内存不足
```bash
# 调整内存配置
export HADOOP_HEAPSIZE=4096
export HIVE_HEAPSIZE=4096
```

### 2. 性能优化

#### 2.1 Hive优化
```sql
-- 启用向量化执行
SET hive.vectorized.execution.enabled=true;
SET hive.vectorized.execution.reduce.enabled=true;

-- 启用CBO优化
SET hive.cbo.enable=true;
```

#### 2.2 分区优化
```sql
-- 分析表统计信息
ANALYZE TABLE fact_watching COMPUTE STATISTICS;

-- 重建分区
ALTER TABLE fact_watching RECOVER PARTITIONS;
```

## 生产环境部署

### 1. 高可用配置

#### 1.1 HDFS高可用
```xml
<!-- hdfs-site.xml -->
<property>
    <name>dfs.nameservices</name>
    <value>mycluster</value>
</property>
<property>
    <name>dfs.ha.namenodes.mycluster</name>
    <value>nn1,nn2</value>
</property>
```

#### 1.2 Hive高可用
```xml
<!-- hive-site.xml -->
<property>
    <name>hive.metastore.uris</name>
    <value>thrift://metastore1:9083,thrift://metastore2:9083</value>
</property>
```

### 2. 安全配置

#### 2.1 Kerberos认证
```bash
# 配置Kerberos
kinit -kt /etc/security/keytabs/hive.service.keytab hive/hostname@REALM
```

#### 2.2 权限控制
```bash
# 设置HDFS权限
hadoop fs -chmod -R 755 /data/video_analysis
hadoop fs -chown -R hive:hive /data/video_analysis
```

### 3. 监控告警

#### 3.1 系统监控
```bash
# 创建监控脚本
cat > scripts/monitor.sh << 'EOF'
#!/bin/bash
# 检查HDFS空间
hdfs_usage=$(hadoop fs -df / | awk 'NR==2{print $5}' | sed 's/%//')
if [ $hdfs_usage -gt 80 ]; then
    echo "HDFS空间使用率过高: ${hdfs_usage}%"
fi

# 检查ETL状态
if [ ! -f logs/etl.log ]; then
    echo "ETL日志文件不存在"
fi
EOF

chmod +x scripts/monitor.sh
```

#### 3.2 定时任务
```bash
# 添加到crontab
(crontab -l ; echo "0 3 * * * /opt/video-platform-rfm-system/scripts/run_complete_analysis.sh") | crontab -
(crontab -l ; echo "0 4 * * * /opt/video-platform-rfm-system/scripts/monitor.sh") | crontab -
```

## 备份和恢复

### 1. 数据备份
```bash
# 备份HDFS数据
hadoop fs -get /data/video_analysis /backup/video_analysis_$(date +%Y%m%d)

# 备份Hive元数据
mysqldump -u root -p metastore > /backup/metastore_$(date +%Y%m%d).sql
```

### 2. 系统恢复
```bash
# 恢复HDFS数据
hadoop fs -put /backup/video_analysis_20240101 /data/video_analysis

# 恢复Hive元数据
mysql -u root -p metastore < /backup/metastore_20240101.sql
```

## 联系支持

如遇到问题，请联系技术支持团队：
- 邮箱: support@video-analysis.com
- 电话: 400-xxx-xxxx
- 文档: https://docs.video-analysis.com
