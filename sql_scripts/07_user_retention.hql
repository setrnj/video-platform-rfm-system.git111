-- 07_user_retention.hql
USE video_analysis;

-- 创建留存率表
CREATE TABLE IF NOT EXISTS user_retention_rate (
    register_date STRING,
    retention_day_7 DECIMAL(5,4)
)
STORED AS ORC;

-- 计算7日留存率
INSERT OVERWRITE TABLE user_retention_rate
SELECT 
    register_date,
    COUNT(CASE WHEN last_active_date >= DATE_ADD(TO_DATE(register_date), 7) THEN phone_no END) * 1.0 /
    COUNT(phone_no) AS retention_day_7
FROM (
    SELECT 
        u.phone_no,  -- 使用手机号作为用户标识
        u.reg_date AS register_date,
        MAX(t.full_date) AS last_active_date
    FROM fact_watching f
    JOIN dim_user u ON f.user_key = u.user_key
    JOIN dim_time t ON f.time_key = t.time_key
    GROUP BY u.phone_no, u.reg_date
) user_activity
GROUP BY register_date
ORDER BY register_date;
