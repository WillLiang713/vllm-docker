#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从魔塔社区(ModelScope)下载模型的脚本
"""

import os
import sys
import signal
import threading
import time
from modelscope import snapshot_download

# 全局变量用于跟踪下载状态
interrupted = False
download_thread = None

def signal_handler(sig, frame):
    """处理Ctrl+C中断信号"""
    global interrupted
    print("\n检测到中断信号，正在停止下载...")
    interrupted = True
    # 强制退出程序
    os._exit(0)

def download_with_interrupt(model_id, local_dir):
    """支持中断的下载函数"""
    global interrupted
    try:
        while not interrupted:
            try:
                model_path = snapshot_download(
                    model_id, 
                    cache_dir=local_dir
                )
                return model_path
            except KeyboardInterrupt:
                print("\n下载被键盘中断")
                interrupted = True
                return None
            except Exception as e:
                if interrupted:
                    return None
                print(f"下载出错: {e}")
                return None
    except Exception as e:
        if not interrupted:
            print(f"下载过程异常: {e}")
        return None

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
        print("按 Ctrl+C 可中断下载")
        
        try:
            model_path = download_with_interrupt(model_id, local_dir)
            
            if model_path is None or interrupted:
                print("下载被取消或中断")
                return None
                
        except KeyboardInterrupt:
            print("\n下载被键盘中断")
            return None
        except Exception as e:
            if not interrupted:
                print(f"下载出错: {e}")
            return None
        
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
    
    try:
        # 下载模型
        download_model(model_id, local_dir)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序执行出错: {e}")
        sys.exit(1)