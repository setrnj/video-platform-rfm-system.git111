# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib as mpl

def generate_hourly_heatmap():
    # 设置中文字体
    try:
        # 尝试使用文泉驿微米黑字体
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        # 回退到默认字体
        print("中文支持警告: 无法设置中文字体，图表中文可能显示异常")
    
    try:
        # 从 HDFS 获取预处理数据
        import subprocess
        subprocess.run(["hdfs", "dfs", "-get", "/results/time_heatmap/000000_0", "time_heatmap.csv"])
        df = pd.read_csv('time_heatmap.csv', 
                         names=['hour_of_day', 'day_of_week', 'sessions', 'avg_duration'])
        
        # 重命名列
        df = df.rename(columns={'sessions': 'active_users'})
        print("成功从 HDFS 获取数据")
    except Exception as e:
        print(f"数据获取失败: {str(e)}")
        print("使用示例数据生成热力图...")
        # 创建示例数据
        data = {
            'hour_of_day': list(range(0, 24)) * 7,
            'day_of_week': [d for d in range(1, 8) for _ in range(24)],
            'active_users': [max(50, (h*10) % 200) for h in range(24*7)]
        }
        df = pd.DataFrame(data)
    
    # 确保目录存在
    os.makedirs("docs", exist_ok=True)
    
    # 转换星期几为中文标签
    #weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    #df['day_of_week'] = df['day_of_week'].apply(
     #   lambda x: weekdays[int(x)-1] if 1 <= int(x) <= 7 else '未知'
    )#
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df['day_of_week'] = df['day_of_week'].apply(lambda x: weekdays[x-1] if 1 <= x <= 7 else "Invalid")
    
    # 创建热力图矩阵
    heatmap_data = df.pivot_table(index="hour_of_day", 
                                 columns="day_of_week", 
                                 values="active_users", 
                                 fill_value=0)
    
    # 简化图表生成
    plt.figure(figsize=(12, 8))
    plt.imshow(heatmap_data, cmap="YlGnBu", aspect='auto')
    plt.colorbar(label='活跃用户数')
    
    # 设置坐标轴
    plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)
    plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns)
    
    plt.title("用户活跃时段热力图")
    plt.xlabel("星期")
    plt.ylabel("小时")
    plt.tight_layout()
    
    plt.savefig("docs/hourly_heatmap_v2.png", dpi=150)
    print("热力图已生成: docs/hourly_heatmap_v2.png")
    
if __name__ == "__main__":
    generate_hourly_heatmap()
