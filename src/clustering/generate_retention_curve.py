import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

subprocess.run(["hdfs", "dfs", "-get", "/results/time_heatmap/000000_0", "time_heatmap.csv"])
df = pd.read_csv('time_heatmap.csv', 
                 names=['week_day', 'hour', 'sessions', 'avg_duration'])



# 加载留存数据
df = pd.read_csv('/results/retention_curve/000000_0', 
                 names=['date', 'day0', 'day1', 'day3', 'day7', 'day14', 'day30'])

# 计算留存率
df['retention_day1'] = df['day1'] / df['day0']
df['retention_day3'] = df['day3'] / df['day0']
df['retention_day7'] = df['day7'] / df['day0']
df['retention_day14'] = df['day14'] / df['day0']
df['retention_day30'] = df['day30'] / df['day0']

# 计算平均留存曲线
avg_retention = df[[
    'retention_day1', 'retention_day3', 
    'retention_day7', 'retention_day14', 
    'retention_day30'
]].mean()

# 创建曲线图
plt.figure(figsize=(12, 7))
days = [1, 3, 7, 14, 30]

# 绘制各日期的留存曲线
for _, row in df.iterrows():
    plt.plot(days, [row[f'retention_day{d}'] for d in [1,3,7,14,30]], 
             color='gray', alpha=0.3, linewidth=1)

# 绘制平均留存曲线
plt.plot(days, avg_retention.values, 
         marker='o', linewidth=3, color='#3498db', 
         label='平均留存率')

# 标注关键点
for i, day in enumerate(days):
    plt.annotate(f'{avg_retention[i]*100:.1f}%', 
                 (day, avg_retention[i]),
                 textcoords="offset points", 
                 xytext=(0,10), 
                 ha='center',
                 fontsize=10)

# 美化图表
plt.title('用户留存曲线 (30天观察期)', fontsize=16)
plt.xlabel('注册后天数', fontsize=12)
plt.ylabel('留存率', fontsize=12)
plt.xticks(days)
plt.ylim(0, 1)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# 添加基准线比较
industry_avg = [0.65, 0.45, 0.35, 0.25, 0.18]
plt.plot(days, industry_avg, 'r--', marker='s', label='行业基准')

# 添加注释框
plt.annotate('关键留存节点:\nDay7留存率预测长期价值', 
             xy=(7, avg_retention[2]), 
             xytext=(10, 0.7), 
             arrowprops=dict(facecolor='black', shrink=0.05),
             fontsize=10)

# 保存结果
plt.tight_layout()
plt.savefig('docs/retention_curve.png', dpi=300)
