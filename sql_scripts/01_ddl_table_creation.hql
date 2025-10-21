USE video_analysis;

-- 确保所有表在创建前删除
DROP TABLE IF EXISTS raw_media;
DROP TABLE IF EXISTS raw_users;
DROP TABLE IF EXISTS cleaned_media;
DROP TABLE IF EXISTS dim_user;
DROP TABLE IF EXISTS dim_time;
DROP TABLE IF EXISTS fact_watching;

-- 原始媒体记录表
CREATE EXTERNAL TABLE raw_media (
  phone_no STRING,
  duration INT,
  station_name STRING,
  origin_time STRING,
  channel_id STRING,
  bitrate STRING,
  network_type STRING
) ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  STORED AS TEXTFILE
  LOCATION '/data/video_analysis/raw/media'
  TBLPROPERTIES ("skip.header.line.count"="1");

-- 原始用户表
CREATE EXTERNAL TABLE raw_users (
  phone_no STRING,
  owner_name STRING,
  run_name STRING,
  sm_name STRING
) ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  STORED AS TEXTFILE
  LOCATION '/data/video_analysis/raw/users'
  TBLPROPERTIES ("skip.header.line.count"="1");

-- 清洗后媒体表 (修正为7列)
CREATE TABLE cleaned_media (
  phone_no STRING,
  duration_sec INT,
  station_name STRING,
  start_time TIMESTAMP,
  channel_id STRING,
  bitrate STRING,
  network_type STRING
) STORED AS ORC;

-- 用户维度表
CREATE TABLE dim_user (
  user_key INT,
  phone_no STRING,
  user_level STRING,
  account_status STRING,
  device_type STRING
) STORED AS ORC;

-- 时间维度表
CREATE TABLE dim_time (
  time_key INT,
  full_time TIMESTAMP,
  hour_of_day INT
) STORED AS ORC;

-- 观看事实表
CREATE TABLE fact_watching (
  user_key INT,
  time_key INT,
  channel_key INT,
  duration_min INT
) STORED AS ORC;
