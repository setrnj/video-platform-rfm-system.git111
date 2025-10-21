import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


subprocess.run(["hdfs", "dfs", "-get", "/results/time_heatmap/000000_0", "time_heatmap.csv"])
df = pd.read_csv('time_heatmap.csv', 
                 names=['week_day', 'hour', 'sessions', 'avg_duration'])

# 加载时段数据
df = pd.read_csv('/results/time_heatmap/000000_0', 
                 names=['week_day', 'hour', 'sessions', 'avg_duration'])

# 转换星期格式
weekday_map = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
df['week_day'] = df['week_day'].map(weekday_map)

# 创建数据透视表
heatmap_data = df.pivot_table(index='hour', columns='week_day', 
                              values='sessions', fill_value=0)

# 排序确保星期顺序正确
heatmap_data = heatmap_data[['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']]

# 创建热力图
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt="d",
            linewidths=.5, cbar_kws={'label': '观看会话数量'})

# 美化图表
plt.title('用户观看行为时段热力图', fontsize=16)
plt.xlabel('星期', fontsize=12)
plt.ylabel('小时', fontsize=12)
plt.xticks(rotation=0)
plt.yticks(rotation=0)

# 添加峰值标注
max_val = heatmap_data.max().max()
max_pos = [(i, j) for i in range(len(heatmap_data.index)) 
           for j in range(len(heatmap_data.columns)) 
           if heatmap_data.iloc[i, j] == max_val]

for pos in max_pos:
    plt.text(pos[1] + 0.5, pos[0] + 0.5, '峰值', 
             ha='center', va='center', color='red', fontsize=10)

# 保存结果
plt.tight_layout()
plt.savefig('docs/hourly_heatmap.png', dpi=300, bbox_inches='tight')
