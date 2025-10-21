from superset import db
from superset.models.core import Database
from superset.models.slice import Slice
from superset.models.dashboard import Dashboard

# 获取数据库
db_obj = db.session.query(Database).filter_by(database_name='video_analysis').first()

# 创建数据集
datasets = [
    {"table_name": "fact_watching", "name": "观看事实表"},
    {"table_name": "dim_user", "name": "用户维度表"},
    {"table_name": "dim_time", "name": "时间维度表"}
]

for ds in datasets:
    dataset = db.session.query(SqlaTable).filter_by(
        table_name=ds["table_name"],
        schema='video_analysis',
        database_id=db_obj.id
    ).first()
    
    if not dataset:
        dataset = SqlaTable(
            table_name=ds["table_name"],
            schema='video_analysis',
            database=db_obj,
            main_dttm_col="start_time" if ds["table_name"] == "fact_watching" else None
        )
        db.session.add(dataset)
        print(f"已创建数据集: {ds['name']}")

db.session.commit()
