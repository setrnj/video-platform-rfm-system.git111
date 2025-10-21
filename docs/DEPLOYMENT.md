# 系统部署清单
## 1. 环境要求
- Hadoop 3.x
- Hive 3.x
- Python 3.6+
- 磁盘空间：>50GB

## 2. 部署步骤
1. 上传项目包到服务器
2. 解压：unzip video-analysis-system.zip
3. 初始化HDFS目录：hadoop fs -mkdir -p /data/video_analysis/{raw,cleaned,dwh}
4. 执行初始ETL：./run_etl.sh
5. 启动Superset：superset run -p 8088

## 3. 验证清单
- [ ] Hive表创建成功
- [ ] 事实表数据量 > 0
- [ ] 仪表盘可访问
- [ ] 日报生成正常
