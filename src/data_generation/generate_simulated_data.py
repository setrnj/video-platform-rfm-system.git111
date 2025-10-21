# generate_simulated_data.py
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# 初始化Faker
fake = Faker('zh_CN')

# 用户相关配置
user_count = 10000
video_count = 500
watch_records = 500000

# 用户等级配置
user_levels = ['青铜', '白银', '黄金', '铂金', '钻石', '星耀', '王者']
level_weights = [0.15, 0.2, 0.25, 0.15, 0.1, 0.1, 0.05]

# 设备类型配置
device_types = ['Android手机', 'iPhone', 'iPad', 'PC网页', '智能电视', '车载设备']
device_weights = [0.4, 0.3, 0.1, 0.1, 0.05, 0.05]

# 影视作品类别配置
video_categories = {
    '电影': ['动作', '喜剧', '爱情', '科幻', '恐怖', '悬疑', '动画', '纪录片'],
    '电视剧': ['古装', '现代', '都市', '历史', '犯罪', '医疗', '校园', '家庭'],
    '综艺': ['选秀', '真人秀', '脱口秀', '竞技', '美食', '旅游', '音乐', '舞蹈'],
    '动漫': ['国产', '日漫', '美漫', '3D', '2D', '热血', '治愈', '冒险'],
    '教育': ['课程', '讲座', '技能', '语言', '考试', '科普', '职场', '儿童']
}

# 平台配置
platforms = ['腾讯视频', '爱奇艺', '优酷', '芒果TV', 'Bilibili', '西瓜视频']

def generate_users():
    """生成用户数据"""
    users = []
    for i in range(user_count):
        users.append({
            'user_id': f'U{i:06d}',
            'phone_no': fake.phone_number(),
            'gender': random.choice(['男', '女']),
            'age': random.randint(18, 60),
            'region': fake.province(),
            'city': fake.city(),
            'user_level': random.choices(user_levels, weights=level_weights)[0],
            'register_date': fake.date_between(start_date='-2y', end_date='today'),
            'device_preference': random.choices(device_types, weights=device_weights)[0]
        })
    return pd.DataFrame(users)

def generate_videos():
    """生成影视作品数据"""
    videos = []
    for i in range(video_count):
        main_category = random.choice(list(video_categories.keys()))
        sub_category = random.choice(video_categories[main_category])
        platform = random.choice(platforms)
        
        videos.append({
            'video_id': f'V{i:06d}',
            'title': f'{main_category}-{sub_category}-{fake.word()}',
            'main_category': main_category,
            'sub_category': sub_category,
            'duration': random.randint(60, 180) if main_category == '电影' else random.randint(30, 60),
            'platform': platform,
            'publish_date': fake.date_between(start_date='-1y', end_date='today'),
            'popularity_score': random.randint(1, 100)
        })
    return pd.DataFrame(videos)

def generate_watch_records(users_df, videos_df):
    """生成观看记录数据"""
    records = []
    user_ids = users_df['user_id'].tolist()
    video_ids = videos_df['video_id'].tolist()
    
    for i in range(watch_records):
        user_id = random.choice(user_ids)
        video_id = random.choice(video_ids)
        user_data = users_df[users_df['user_id'] == user_id].iloc[0]
        video_data = videos_df[videos_df['video_id'] == video_id].iloc[0]
        
        # 基于用户等级和设备类型调整观看行为
        watch_duration = random.randint(5, video_data['duration'])
        if user_data['user_level'] in ['钻石', '星耀', '王者']:
            watch_duration = min(watch_duration + random.randint(10, 30), video_data['duration'])
        
        records.append({
            'record_id': f'R{i:08d}',
            'user_id': user_id,
            'video_id': video_id,
            'watch_date': fake.date_time_between(start_date='-30d', end_date='now'),
            'watch_duration': watch_duration,
            'device_type': user_data['device_preference'],
            'network_type': random.choice(['4G', '5G', 'WIFI', '有线']),
            'complete_rate': watch_duration / video_data['duration']
        })
    return pd.DataFrame(records)

def generate_category_rankings(videos_df, watch_df):
    """生成各类别榜单"""
    # 合并数据
    merged_df = watch_df.merge(videos_df, on='video_id')
    
    # 总观看时长榜单
    total_watch_rank = merged_df.groupby(['main_category', 'sub_category']).agg({
        'watch_duration': 'sum',
        'record_id': 'count'
    }).reset_index()
    total_watch_rank = total_watch_rank.sort_values('watch_duration', ascending=False)
    
    # 平台热门内容榜单
    platform_rank = merged_df.groupby(['platform', 'main_category']).agg({
        'watch_duration': 'sum',
        'record_id': 'count'
    }).reset_index()
    platform_rank = platform_rank.sort_values('watch_duration', ascending=False)
    
    # 用户等级偏好榜单
    user_watch_rank = merged_df.merge(users_df, on='user_id').groupby(['user_level', 'main_category']).agg({
        'watch_duration': 'sum',
        'record_id': 'count'
    }).reset_index()
    user_watch_rank = user_watch_rank.sort_values('watch_duration', ascending=False)
    
    return total_watch_rank, platform_rank, user_watch_rank

if __name__ == "__main__":
    print("开始生成模拟数据...")
    
    # 生成用户数据
    print("生成用户数据...")
    users_df = generate_users()
    users_df.to_csv('data/simulated_users.csv', index=False, encoding='utf-8')
    
    # 生成视频数据
    print("生成影视作品数据...")
    videos_df = generate_videos()
    videos_df.to_csv('data/simulated_videos.csv', index=False, encoding='utf-8')
    
    # 生成观看记录
    print("生成观看记录数据...")
    watch_df = generate_watch_records(users_df, videos_df)
    watch_df.to_csv('data/simulated_watch_records.csv', index=False, encoding='utf-8')
    
    # 生成榜单数据
    print("生成各类榜单...")
    total_rank, platform_rank, user_rank = generate_category_rankings(videos_df, watch_df)
    
    total_rank.to_csv('data/category_ranking.csv', index=False, encoding='utf-8')
    platform_rank.to_csv('data/platform_ranking.csv', index=False, encoding='utf-8')
    user_rank.to_csv('data/user_level_ranking.csv', index=False, encoding='utf-8')
    
    print("数据生成完成！")
    print(f"用户数量: {len(users_df)}")
    print(f"视频数量: {len(videos_df)}")
    print(f"观看记录: {len(watch_df)}")
    
    # 输出一些统计信息
    print("\n=== 数据统计 ===")
    print("用户等级分布:")
    print(users_df['user_level'].value_counts())
    print("\n设备类型分布:")
    print(users_df['device_preference'].value_counts())
    print("\n影视类别分布:")
    print(videos_df['main_category'].value_counts())
