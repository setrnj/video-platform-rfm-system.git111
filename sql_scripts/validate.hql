-- 修正后的 validate.hql
SELECT 
  'cleaned_media' AS tbl,  -- 将 table 改为 tbl
  COUNT(*) AS cnt 
FROM video_analysis.cleaned_media
UNION ALL
SELECT 'dim_user', COUNT(*) FROM video_analysis.dim_user
UNION ALL
SELECT 'fact_watching', COUNT(*) FROM video_analysis.fact_watching;
