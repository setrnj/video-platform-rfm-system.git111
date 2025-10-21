#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表生成器
Chart Generator
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import yaml

class ChartGenerator:
    """图表生成器"""
    
    def __init__(self, config):
        """初始化图表生成器"""
        self.config = config
        self.setup_style()
        
    def setup_style(self):
        """设置图表样式"""
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.style.use('seaborn-v0_8')
        
    def generate_heatmap(self):
        """生成时段热力图"""
        print("生成时段热力图...")
        
        # 模拟时段数据
        hours = list(range(24))
        days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        # 生成模拟数据
        np.random.seed(42)
        data = np.random.poisson(100, (7, 24))
        
        # 创建热力图
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(data, 
                    xticklabels=hours,
                    yticklabels=days,
                    cmap='YlOrRd',
                    annot=True,
                    fmt='d',
                    cbar_kws={'label': '观看次数'})
        
        ax.set_title('用户观看行为时段热力图', fontsize=16, fontweight='bold')
        ax.set_xlabel('小时', fontsize=12)
        ax.set_ylabel('星期', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('outputs/charts/hourly_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("时段热力图已保存到 outputs/charts/hourly_heatmap.png")
    
    def generate_retention_curve(self):
        """生成留存曲线"""
        print("生成留存曲线...")
        
        # 模拟留存数据
        periods = [1, 3, 7, 14, 30]
        retention_rates = [100, 85, 70, 55, 40]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(periods, retention_rates, 'o-', linewidth=2, markersize=8, color='#2E86AB')
        ax.fill_between(periods, retention_rates, alpha=0.3, color='#2E86AB')
        
        ax.set_title('用户留存曲线', fontsize=16, fontweight='bold')
        ax.set_xlabel('留存天数', fontsize=12)
        ax.set_ylabel('留存率 (%)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        
        # 添加数据标签
        for i, (period, rate) in enumerate(zip(periods, retention_rates)):
            ax.annotate(f'{rate}%', (period, rate), 
                       textcoords="offset points", xytext=(0,10), ha='center')
        
        plt.tight_layout()
        plt.savefig('outputs/charts/retention_curve.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("留存曲线已保存到 outputs/charts/retention_curve.png")
    
    def generate_rfm_distribution(self):
        """生成RFM分布图"""
        print("生成RFM分布图...")
        
        # 模拟RFM数据
        np.random.seed(42)
        n_users = 1000
        
        rfm_data = {
            'Recency': np.random.normal(15, 10, n_users),
            'Frequency': np.random.poisson(5, n_users),
            'Monetary': np.random.exponential(100, n_users)
        }
        
        df = pd.DataFrame(rfm_data)
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # R分布
        axes[0, 0].hist(df['Recency'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('最近活跃度分布 (R)', fontweight='bold')
        axes[0, 0].set_xlabel('天数')
        axes[0, 0].set_ylabel('用户数量')
        
        # F分布
        axes[0, 1].hist(df['Frequency'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('观看频次分布 (F)', fontweight='bold')
        axes[0, 1].set_xlabel('次数')
        axes[0, 1].set_ylabel('用户数量')
        
        # M分布
        axes[1, 0].hist(df['Monetary'], bins=30, alpha=0.7, color='salmon', edgecolor='black')
        axes[1, 0].set_title('观看时长分布 (M)', fontweight='bold')
        axes[1, 0].set_xlabel('分钟')
        axes[1, 0].set_ylabel('用户数量')
        
        # RFM相关性
        correlation = df.corr()
        im = axes[1, 1].imshow(correlation, cmap='coolwarm', aspect='auto')
        axes[1, 1].set_xticks(range(len(correlation.columns)))
        axes[1, 1].set_yticks(range(len(correlation.columns)))
        axes[1, 1].set_xticklabels(correlation.columns)
        axes[1, 1].set_yticklabels(correlation.columns)
        axes[1, 1].set_title('RFM相关性矩阵', fontweight='bold')
        
        # 添加相关系数标签
        for i in range(len(correlation.columns)):
            for j in range(len(correlation.columns)):
                text = axes[1, 1].text(j, i, f'{correlation.iloc[i, j]:.2f}',
                                      ha="center", va="center", color="black")
        
        plt.tight_layout()
        plt.savefig('outputs/charts/rfm_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("RFM分布图已保存到 outputs/charts/rfm_distribution.png")
    
    def generate_all_charts(self):
        """生成所有图表"""
        print("开始生成所有可视化图表...")
        
        # 创建输出目录
        import os
        os.makedirs('outputs/charts', exist_ok=True)
        os.makedirs('outputs/reports', exist_ok=True)
        
        # 生成各种图表
        self.generate_heatmap()
        self.generate_retention_curve()
        self.generate_rfm_distribution()
        
        print("所有图表生成完成！")
        print("图表保存位置: outputs/charts/")
