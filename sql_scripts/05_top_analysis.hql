-- 05_top_analysis.hql
USE video_analysis;

-- 获取当前日期
SET hivevar:current_date = CURRENT_DATE();

-- 用户行为分析
INSERT OVERWRITE LOCAL DIRECTORY '/root/video-behavior-analysis/results/user_behavior_tmp'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT 
  u.province,
  u.city,
  u.age,
  u.gender,
  SUM(f.duration_min) AS total_duration,
  COUNT(1) AS watch_count
FROM fact_watching f
JOIN dim_user u ON f.user_key = u.user_key
GROUP BY u.province, u.city, u.age, u.gender;

-- 热门用户分析
INSERT OVERWRITE LOCAL DIRECTORY '/root/video-behavior-analysis/results/top_users_tmp'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT 
  u.phone_no,
  u.province,
  u.city,
  SUM(f.duration_min) AS total_duration
FROM fact_watching f
JOIN dim_user u ON f.user_key = u.user_key
GROUP BY u.phone_no, u.province, u.city
ORDER BY total_duration DESC
LIMIT 10;
-- 新增RFM用户分群计算
DROP TABLE IF EXISTS user_rfm_analysis;
CREATE TABLE user_rfm_analysis STORED AS ORC AS
SELECT 
  phone_no,
  recency_days,
  frequency,
  monetary,
  r_score,
  f_score,
  m_score,
  CONCAT(r_score, f_score, m_score) AS rfm_cell
FROM (
  SELECT 
    u.phone_no,
    DATEDIFF(CURRENT_DATE, MAX(t.full_time)) AS recency_days,
    COUNT(*) AS frequency,
    SUM(f.duration_min) AS monetary,
    NTILE(5) OVER(ORDER BY DATEDIFF(CURRENT_DATE, MAX(t.full_time)) DESC) AS r_score,
    NTILE(5) OVER(ORDER BY COUNT(*) DESC) AS f_score,
    NTILE(5) OVER(ORDER BY SUM(f.duration_min) DESC) AS m_score
  FROM fact_watching f
  JOIN dim_user u ON f.user_key = u.user_key
  JOIN dim_time t ON f.time_key = t.time_key
  GROUP BY u.phone_no
) subquery;

-- 导出结果到CSV
INSERT OVERWRITE DIRECTORY '/results/user_rfm'
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT * FROM user_rfm_analysis;
