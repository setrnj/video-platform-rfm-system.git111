USE video_analysis;

-- 新增时段热力数据
-- 新增时段热力数据
DROP TABLE IF EXISTS time_heatmap_data;
CREATE TABLE time_heatmap_data STORED AS ORC AS
SELECT 
  t.hour_of_day,  -- 修正列名
  COUNT(*) AS session_count,
  AVG(f.duration_min) AS avg_duration
FROM fact_watching f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.hour_of_day;

-- 导出结果
INSERT OVERWRITE DIRECTORY '/results/time_heatmap'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT * FROM time_heatmap_data;

-- 修正后的留存曲线数据
DROP TABLE IF EXISTS retention_curve_data;
CREATE TABLE retention_curve_data STORED AS ORC AS
WITH first_activity AS (
  SELECT 
    u.phone_no,
    MIN(t.full_time) AS first_day
  FROM fact_watching f
  JOIN dim_user u ON f.user_key = u.user_key
  JOIN dim_time t ON f.time_key = t.time_key
  GROUP BY u.phone_no
)
SELECT 
  first_day,
  COUNT(DISTINCT CASE WHEN days_since_first = 0 THEN phone_no END) AS day0,
  COUNT(DISTINCT CASE WHEN days_since_first = 1 THEN phone_no END) AS day1,
  COUNT(DISTINCT CASE WHEN days_since_first = 3 THEN phone_no END) AS day3,
  COUNT(DISTINCT CASE WHEN days_since_first = 7 THEN phone_no END) AS day7,
  COUNT(DISTINCT CASE WHEN days_since_first = 14 THEN phone_no END) AS day14,
  COUNT(DISTINCT CASE WHEN days_since_first = 30 THEN phone_no END) AS day30
FROM (
  SELECT 
    fa.phone_no,  -- 使用fa别名
    fa.first_day,
    DATEDIFF(t.full_time, fa.first_day) AS days_since_first
  FROM fact_watching f
  JOIN dim_user u ON f.user_key = u.user_key
  JOIN dim_time t ON f.time_key = t.time_key
  JOIN first_activity fa ON u.phone_no = fa.phone_no
) activity
GROUP BY first_day
ORDER BY first_day DESC
LIMIT 30;

-- 导出结果
INSERT OVERWRITE DIRECTORY '/results/retention_curve'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT * FROM retention_curve_data;
