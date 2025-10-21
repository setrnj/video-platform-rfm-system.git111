#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RFM分析计算器
RFM Analysis Calculator
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pyhive import hive
import yaml

class RFMCalculator:
    """RFM分析计算器"""
    
    def __init__(self, config):
        """初始化RFM计算器"""
        self.config = config
        self.connection = None
        
    def connect_hive(self):
        """连接Hive数据库"""
        try:
            self.connection = hive.Connection(
                host='localhost',
                port=10000,
                database='video_analysis'
            )
            print("Hive连接成功")
        except Exception as e:
            print(f"Hive连接失败: {e}")
            raise
    
    def calculate_recency(self):
        """计算最近活跃度(R)"""
        query = """
        SELECT 
            user_key,
            DATEDIFF(CURRENT_DATE(), MAX(full_time)) as recency_days
        FROM fact_watching fw
        JOIN dim_time dt ON fw.time_key = dt.time_key
        GROUP BY user_key
        """
        return pd.read_sql(query, self.connection)
    
    def calculate_frequency(self):
        """计算频次(F)"""
        query = """
        SELECT 
            user_key,
            COUNT(*) as frequency
        FROM fact_watching
        GROUP BY user_key
        """
        return pd.read_sql(query, self.connection)
    
    def calculate_monetary(self):
        """计算价值(M)"""
        query = """
        SELECT 
            user_key,
            SUM(duration_min) as monetary_value
        FROM fact_watching
        GROUP BY user_key
        """
        return pd.read_sql(query, self.connection)
    
    def calculate_rfm_scores(self):
        """计算RFM分数"""
        print("开始计算RFM分数...")
        
        # 连接数据库
        self.connect_hive()
        
        # 计算R、F、M
        recency_df = self.calculate_recency()
        frequency_df = self.calculate_frequency()
        monetary_df = self.calculate_monetary()
        
        # 合并数据
        rfm_df = recency_df.merge(frequency_df, on='user_key')
        rfm_df = rfm_df.merge(monetary_df, on='user_key')
        
        # 计算RFM分数（1-5分）
        rfm_df['R_score'] = pd.qcut(rfm_df['recency_days'], 5, labels=[5,4,3,2,1])
        rfm_df['F_score'] = pd.qcut(rfm_df['frequency'], 5, labels=[1,2,3,4,5])
        rfm_df['M_score'] = pd.qcut(rfm_df['monetary_value'], 5, labels=[1,2,3,4,5])
        
        # 保存结果
        rfm_df.to_csv('data/results/rfm_scores.csv', index=False)
        print("RFM分数计算完成，结果保存到 data/results/rfm_scores.csv")
        
        return rfm_df
    
    def segment_users(self, rfm_df):
        """用户分群"""
        print("开始用户分群...")
        
        # 定义分群规则
        segments = self.config['rfm_analysis']['segments']
        
        def assign_segment(row):
            r, f, m = row['R_score'], row['F_score'], row['M_score']
            
            for segment_name, rules in segments.items():
                if (r in rules['recency'] and 
                    f in rules['frequency'] and 
                    m in rules['monetary']):
                    return segment_name
            return 'other'
        
        rfm_df['segment'] = rfm_df.apply(assign_segment, axis=1)
        
        # 保存分群结果
        rfm_df.to_csv('data/results/user_segments.csv', index=False)
        print("用户分群完成，结果保存到 data/results/user_segments.csv")
        
        return rfm_df
