#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频平台RFM分析系统主程序
Video Platform RFM Analysis System Main Program
"""

import sys
import os
import argparse
import yaml
from datetime import datetime

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def load_config(config_file):
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_etl_pipeline():
    """执行ETL流程"""
    print("执行ETL流程...")
    os.system("bash scripts/run_etl.sh")

def run_rfm_analysis():
    """执行RFM分析"""
    print("执行RFM分析...")
    from rfm_analysis.rfm_calculator import RFMCalculator
    from clustering.user_segmentation import UserSegmentation
    
    # 加载配置
    rfm_config = load_config('config/rfm_config.yaml')
    
    # 执行RFM分析
    rfm_calc = RFMCalculator(rfm_config)
    rfm_calc.calculate_rfm_scores()
    
    # 执行用户分群
    segmentation = UserSegmentation(rfm_config)
    segmentation.perform_clustering()

def run_visualization():
    """执行可视化生成"""
    print("生成可视化图表...")
    from visualization.chart_generator import ChartGenerator
    
    # 加载配置
    viz_config = load_config('config/visualization_config.yaml')
    
    # 生成图表
    chart_gen = ChartGenerator(viz_config)
    chart_gen.generate_all_charts()

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='视频平台RFM分析系统')
    parser.add_argument('--mode', choices=['etl', 'rfm', 'viz', 'all'], 
                       default='all', help='运行模式')
    parser.add_argument('--config', default='config', 
                       help='配置文件目录')
    parser.add_argument('--generate-data', action='store_true',
                       help='生成模拟数据')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("视频平台RFM分析系统")
    print("Video Platform RFM Analysis System")
    print("=" * 50)
    print(f"运行模式: {args.mode}")
    print(f"开始时间: {datetime.now()}")
    print("=" * 50)
    
    try:
        if args.mode in ['etl', 'all']:
            run_etl_pipeline()
            
        if args.mode in ['rfm', 'all']:
            run_rfm_analysis()
            
        if args.mode in ['viz', 'all']:
            run_visualization()
            
        print("=" * 50)
        print("分析完成！")
        print(f"结束时间: {datetime.now()}")
        print("=" * 50)
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
