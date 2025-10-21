USE video_analysis;

-- 确保使用正确的列数和列名
INSERT OVERWRITE TABLE cleaned_media
SELECT 
  phone_no,
  CASE 
    WHEN duration <= 0 THEN 0 
    WHEN duration > 86400 THEN 86400
    ELSE duration 
  END AS duration_sec,
  TRIM(LOWER(station_name)) AS station_name,
  CAST(FROM_UNIXTIME(UNIX_TIMESTAMP(origin_time, 'yyyy-MM-dd HH:mm:ss')) AS TIMESTAMP) AS start_time,
  channel_id,
  bitrate,
  network_type
FROM raw_media
WHERE phone_no RLIKE '^1[3-9]\\d{9}$'  -- 修正正则表达式转义
  AND phone_no IS NOT NULL
  AND origin_time IS NOT NULL;

-- 验证清洗后数据
SELECT 'cleaned_media' AS table_name, COUNT(*) AS row_count FROM cleaned_media;
