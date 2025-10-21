import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

plt.figure(figsize=(12, 8))
ax = plt.subplot(111)

# 绘制事实表
ax.add_patch(Rectangle((0.3, 0.4), 0.4, 0.2, fill=True, color='lightblue'))
plt.text(0.5, 0.5, 'fact_watching\n(观看事实表)', ha='center', va='center')

# 绘制维度表
dim_tables = [
    (0.1, 0.7, 'dim_user\n(用户维度)'),
    (0.7, 0.7, 'dim_time\n(时间维度)'),
    (0.1, 0.1, 'dim_program\n(节目维度)'),
    (0.7, 0.1, 'dim_channel\n(频道维度)')
]

for x, y, label in dim_tables:
    ax.add_patch(Rectangle((x, y), 0.2, 0.15, fill=True, color='lightgreen'))
    plt.text(x+0.1, y+0.075, label, ha='center', va='center')

# 绘制关联线
connections = [
    (0.3, 0.5, 0.2, 0.775),  # fact->user
    (0.5, 0.5, 0.6, 0.775),  # fact->time
    (0.3, 0.4, 0.2, 0.15),   # fact->program
    (0.5, 0.4, 0.6, 0.15)    # fact->channel
]

for x1,y1,x2,y2 in connections:
    plt.plot([x1, x2], [y1, y2], 'k-', lw=1.5)
    plt.plot([x2], [y2], 'ko', markersize=5)

plt.axis('off')
plt.title('数据仓库星型模型', fontsize=16)
plt.savefig('docs/er_diagram.png', dpi=300, bbox_inches='tight')
