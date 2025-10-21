import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# 创建图表输出目录
os.makedirs('docs', exist_ok=True)

# 1. 用户观看时长分布图
print("正在生成用户观看时长分布图...")
try:
    # 生成模拟数据
    np.random.seed(42)
    data = np.random.gamma(2, 1.5, 1000) * 15
    df = pd.DataFrame(data, columns=['duration_min'])
    
    plt.figure(figsize=(10,6))
    sns.histplot(data=df, x='duration_min', bins=50, kde=True)
    plt.title('用户单次观看时长分布')
    plt.xlabel('时长(分钟)')
    plt.savefig('docs/duration_distribution.png', dpi=300, bbox_inches='tight')
    print("已生成: docs/duration_distribution.png")
except Exception as e:
    print(f"生成时长分布图失败: {str(e)}")

# 2. 时段热力图
print("正在生成时段热力图...")
try:
    # 生成模拟数据
    hours = np.tile(np.arange(24), 7)
    weekdays = np.repeat(np.arange(1, 8), 24)
    sessions = np.random.poisson(50, 168) + (weekdays < 6) * np.random.randint(20, 40, 168)
    sessions += (hours >= 19) * np.random.randint(30, 60, 168)
    sessions += (hours >= 12) * (hours <= 14) * np.random.randint(20, 40, 168)
    
    df = pd.DataFrame({
        'hour': hours,
        'weekday': weekdays,
        'sessions': sessions
    })
    
    pivot = df.pivot_table(
        index='hour', 
        columns='weekday', 
        values='sessions', 
        fill_value=0
    )
    
    plt.figure(figsize=(12,8))
    sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt='d')
    plt.title('24小时观看分布（按星期几）')
    plt.xlabel('星期几')
    plt.ylabel('小时')
    plt.savefig('docs/hourly_heatmap.png', dpi=300, bbox_inches='tight')
    print("已生成: docs/hourly_heatmap.png")
except Exception as e:
    print(f"生成时段热力图失败: {str(e)}")

# 3. 用户留存曲线
print("正在生成留存曲线图...")
try:
    # 生成模拟数据
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    rates = np.clip(0.6 + np.random.normal(0, 0.05, 30) + 
                   np.sin(np.linspace(0, 2*np.pi, 30)) * 0.1, 0.5, 0.75)
    
    df = pd.DataFrame({
        'date': dates,
        'rate': rates
    })
    
    plt.figure(figsize=(10,6))
    plt.plot(df['date'], df['rate'], marker='o')
    plt.title('7日用户留存率趋势')
    plt.xlabel('日期')
    plt.ylabel('留存率')
    plt.ylim(0.4, 0.8)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('docs/retention_trend.png', dpi=300, bbox_inches='tight')
    print("已生成: docs/retention_trend.png")
except Exception as e:
    print(f"生成留存曲线失败: {str(e)}")

print("图表生成完成!")
