INSERT OVERWRITE LOCAL DIRECTORY 'results/user_behavior' 
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
    SELECT * FROM ( ... );
USE video_analysis;

-- 时段分析 (修正列引用)
SELECT 
  t.hour_of_day,
  AVG(f.duration_min) AS avg_duration,
  COUNT(*) AS session_count
FROM fact_watching f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.hour_of_day
ORDER BY t.hour_of_day;

-- 设备类型分析 (修正列引用)
SELECT 
  u.device_type,
  COUNT(*) AS sessions,
  AVG(f.duration_min) AS avg_duration
FROM fact_watching f
JOIN dim_user u ON f.user_key = u.user_key  -- 修正为u.user_key
GROUP BY u.device_type;
