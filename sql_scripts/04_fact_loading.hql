-- 04_fact_loading.hql (最终版)
SET hive.auto.convert.join=true;
SET hive.exec.dynamic.partition.mode=nonstrict;
USE video_analysis;

-- 加载事实表
INSERT OVERWRITE TABLE fact_watching
SELECT 
  u.user_key,
  t.time_key,
  1 AS channel_key,
  cm.duration_sec / 60.0 AS duration_min
FROM cleaned_media cm
JOIN dim_user u ON cm.phone_no = u.phone_no
JOIN dim_time t 
  -- 使用原始字符串比较
  ON cm.start_time = t.full_time;
