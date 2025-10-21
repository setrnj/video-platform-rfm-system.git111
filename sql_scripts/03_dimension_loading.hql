USE video_analysis;

-- 删除旧表
DROP TABLE IF EXISTS dim_user;

-- 创建维度表
CREATE TABLE dim_user (
  user_key BIGINT,
  phone_no STRING,
  province STRING,
  city STRING,
  age INT,
  gender STRING,
  reg_date STRING,
  vip_expire_date STRING
) STORED AS ORC;

-- 插入数据（关键修正）
INSERT INTO TABLE dim_user
SELECT 
  ROW_NUMBER() OVER(ORDER BY phone_no) AS user_key,
  phone_no,
  CASE 
    WHEN substr(phone_no, 1, 3) = '138' THEN '广东'
    WHEN substr(phone_no, 1, 3) = '139' THEN '浙江'
    ELSE '其他' 
  END AS province,
  CASE 
    WHEN substr(phone_no, 1, 3) = '138' THEN '广州'
    WHEN substr(phone_no, 1, 3) = '139' THEN '杭州'
    ELSE '未知' 
  END AS city,
  FLOOR(RAND() * 30) + 18 AS age,
  CASE WHEN RAND() > 0.5 THEN 'M' ELSE 'F' END AS gender,
  -- 注册日期：当前日期减去随机天数
  DATE_SUB(CURRENT_DATE(), CAST(FLOOR(RAND() * 365) AS INT)) AS reg_date,
  -- VIP过期日期：注册日期 + 365天（使用DATE_ADD + 显式类型转换）
  DATE_ADD(
    DATE_SUB(CURRENT_DATE(), CAST(FLOOR(RAND() * 365) AS INT)), 
    CAST(365 AS INT)
  ) AS vip_expire_date
FROM (
  SELECT DISTINCT phone_no 
  FROM cleaned_media
  WHERE phone_no IS NOT NULL AND phone_no != ''
) t;
-- 创建时间维度表
DROP TABLE IF EXISTS dim_time;
CREATE TABLE dim_time (
  time_key INT,
  full_time TIMESTAMP,
  hour_of_day INT
) STORED AS ORC;

-- 加载时间维度数据（生成2025年全年的时间数据）
INSERT INTO TABLE dim_time
SELECT 
  ROW_NUMBER() OVER(ORDER BY t.full_time) AS time_key,
  t.full_time,
  HOUR(t.full_time) AS hour_of_day
FROM (
  SELECT 
    from_unixtime(unix_timestamp('2025-01-01 00:00:00') + (t1.pos * 3600)) AS full_time
  FROM (
    SELECT posexplode(split(space(365*24-1), ' ')) AS (pos, val) -- 365天*24小时
  ) t1
) t;
