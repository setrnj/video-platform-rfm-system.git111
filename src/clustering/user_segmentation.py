#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户分群模块
User Segmentation Module
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import yaml

class UserSegmentation:
    """用户分群分析"""
    
    def __init__(self, config):
        """初始化用户分群"""
        self.config = config
        self.scaler = StandardScaler()
        
    def load_rfm_data(self):
        """加载RFM数据"""
        try:
            df = pd.read_csv('data/results/rfm_scores.csv')
            print(f"加载RFM数据: {len(df)} 条记录")
            return df
        except FileNotFoundError:
            print("RFM数据文件不存在，请先运行RFM分析")
            return None
    
    def perform_clustering(self):
        """执行K-means聚类"""
        print("开始用户聚类分析...")
        
        # 加载数据
        df = self.load_rfm_data()
        if df is None:
            return
        
        # 准备特征数据
        features = ['recency_days', 'frequency', 'monetary_value']
        X = df[features].values
        
        # 标准化数据
        X_scaled = self.scaler.fit_transform(X)
        
        # K-means聚类
        n_clusters = self.config['clustering']['n_clusters']
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # 分析聚类结果
        self.analyze_clusters(df)
        
        # 生成可视化
        self.generate_cluster_visualization(df)
        
        # 生成报告
        self.generate_segmentation_report(df)
        
        # 保存结果
        df.to_csv('data/results/clustered_users.csv', index=False)
        print("用户聚类分析完成")
        
        return df
    
    def analyze_clusters(self, df):
        """分析聚类结果"""
        print("\n=== 聚类结果分析 ===")
        
        cluster_summary = df.groupby('cluster').agg({
            'recency_days': ['mean', 'std'],
            'frequency': ['mean', 'std'],
            'monetary_value': ['mean', 'std'],
            'user_key': 'count'
        }).round(2)
        
        print(cluster_summary)
        
        # 定义聚类标签
        cluster_labels = {
            0: "低价值用户",
            1: "潜力用户", 
            2: "活跃用户",
            3: "高价值用户"
        }
        
        df['cluster_label'] = df['cluster'].map(cluster_labels)
        
        # 保存聚类摘要
        cluster_summary.to_csv('data/results/cluster_summary.csv')
        
    def generate_cluster_visualization(self, df):
        """生成聚类可视化"""
        print("生成聚类可视化图表...")
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # RFM散点图
        axes[0, 0].scatter(df['recency_days'], df['monetary_value'], 
                          c=df['cluster'], cmap='viridis', alpha=0.6)
        axes[0, 0].set_xlabel('最近活跃天数')
        axes[0, 0].set_ylabel('观看时长(分钟)')
        axes[0, 0].set_title('用户聚类分布 (R-M)')
        
        # 频次-价值散点图
        axes[0, 1].scatter(df['frequency'], df['monetary_value'], 
                          c=df['cluster'], cmap='viridis', alpha=0.6)
        axes[0, 1].set_xlabel('观看频次')
        axes[0, 1].set_ylabel('观看时长(分钟)')
        axes[0, 1].set_title('用户聚类分布 (F-M)')
        
        # 聚类分布饼图
        cluster_counts = df['cluster_label'].value_counts()
        axes[1, 0].pie(cluster_counts.values, labels=cluster_counts.index, 
                       autopct='%1.1f%%', startangle=90)
        axes[1, 0].set_title('用户分群比例')
        
        # RFM雷达图
        cluster_means = df.groupby('cluster_label')[['recency_days', 'frequency', 'monetary_value']].mean()
        cluster_means = cluster_means.div(cluster_means.max())  # 归一化
        
        for i, (cluster, values) in enumerate(cluster_means.iterrows()):
            axes[1, 1].plot(['R', 'F', 'M'], values.values, 
                           marker='o', label=cluster, linewidth=2)
        
        axes[1, 1].set_title('各分群RFM特征对比')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('outputs/charts/user_segmentation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("聚类可视化图表已保存到 outputs/charts/user_segmentation.png")
    
    def generate_segmentation_report(self, df):
        """生成分群报告"""
        print("生成用户分群报告...")
        
        # 创建PDF报告
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, '用户分群分析报告', 0, 1, 'C')
        pdf.ln(10)
        
        # 添加聚类统计
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '聚类统计信息', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        cluster_stats = df.groupby('cluster_label').size()
        for cluster, count in cluster_stats.items():
            percentage = count / len(df) * 100
            pdf.cell(0, 8, f'{cluster}: {count} 用户 ({percentage:.1f}%)', 0, 1)
        
        pdf.ln(10)
        
        # 添加特征分析
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, '各分群特征分析', 0, 1)
        pdf.set_font('Arial', '', 10)
        
        for cluster in df['cluster_label'].unique():
            cluster_data = df[df['cluster_label'] == cluster]
            pdf.cell(0, 8, f'{cluster}:', 0, 1)
            pdf.cell(0, 6, f'  平均活跃天数: {cluster_data["recency_days"].mean():.1f}', 0, 1)
            pdf.cell(0, 6, f'  平均观看频次: {cluster_data["frequency"].mean():.1f}', 0, 1)
            pdf.cell(0, 6, f'  平均观看时长: {cluster_data["monetary_value"].mean():.1f}分钟', 0, 1)
            pdf.ln(5)
        
        # 保存报告
        pdf.output('outputs/reports/user_segmentation_report.pdf')
        print("用户分群报告已保存到 outputs/reports/user_segmentation_report.pdf")
