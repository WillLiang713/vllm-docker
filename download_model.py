#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从魔塔社区(ModelScope)下载模型的脚本
"""

import os
import sys
from modelscope import snapshot_download

def download_model(model_id, local_dir="./models"):
    """
    从ModelScope下载模型
    
    Args:
        model_id (str): 模型ID，例如 "qwen/Qwen3-0.6B"
        local_dir (str): 本地存储目录，默认为 "./models"
    
    Returns:
        str: 模型存储路径
    """
    try:
        # 创建本地目录（如果不存在）
        os.makedirs(local_dir, exist_ok=True)
        
        # 下载模型
        print(f"开始下载模型: {model_id}")
        print(f"存储路径: {local_dir}")
        
        model_path = snapshot_download(
            model_id, 
            cache_dir=local_dir
        )
        
        print(f"模型下载完成，存储在: {model_path}")
        return model_path
        
    except Exception as e:
        print(f"下载模型时出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 默认下载Qwen3-0.6B模型
    model_id = "qwen/Qwen3-0.6B"
    local_dir = "./models"
    
    # 如果提供了命令行参数，则使用参数指定的模型
    if len(sys.argv) > 1:
        model_id = sys.argv[1]
    
    if len(sys.argv) > 2:
        local_dir = sys.argv[2]
    
    # 下载模型
    download_model(model_id, local_dir)