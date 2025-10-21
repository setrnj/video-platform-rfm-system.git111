from superset import db
from superset.models.core import Database

hive_db = Database(
    database_name='video_analysis',
    sqlalchemy_uri='hive://localhost:10000/video_analysis'
)
db.session.add(hive_db)
db.session.commit()
print("Hive数据库连接已创建")
