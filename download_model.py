#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从魔塔社区(ModelScope)下载模型的脚本,支持断点续传和完整性校验"""

import argparse
import os
import sys
from modelscope import snapshot_download
from modelscope.hub.api import HubApi

DEFAULT_MODEL = "qwen/Qwen3-0.6B"
DEFAULT_DIR = "./models"

def verify_model(model_id, local_dir):
    """校验模型文件完整性"""
    try:
        model_files = HubApi().get_model_files(model_id)
        model_dir = os.path.join(local_dir, model_id)
        
        if not os.path.exists(model_dir):
            print(f"未找到模型目录: {model_dir}")
            return False

        print(f"正在校验 {len(model_files)} 个文件...")
        
        for i, file_info in enumerate(model_files, 1):
            file_path = os.path.join(model_dir, file_info['Path'])
            if not os.path.exists(file_path) or (file_info.get('Size', 0) > 0 and os.path.getsize(file_path) != file_info['Size']):
                print(f"[{i}/{len(model_files)}] 文件问题: {file_info['Path']}")
                return False

        print("所有文件校验通过")
        return True
    except Exception as e:
        print(f"校验失败: {e}")
        return False

def download_model(model_id, local_dir=DEFAULT_DIR, verify=True):
    """从ModelScope下载模型,支持断点续传"""
    os.makedirs(local_dir, exist_ok=True)
    print(f"开始下载模型: {model_id}\n存储路径: {local_dir}\n")
    
    model_path = snapshot_download(model_id, cache_dir=local_dir)
    print(f"\n模型下载完成: {model_path}")

    if verify and not verify_model(model_id, local_dir):
        print("✗ 模型可能不完整,建议重新下载")
        return None
    
    print("✓ 模型下载完整" if verify else "")
    return model_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从ModelScope下载模型")
    parser.add_argument("model", nargs="?", default=DEFAULT_MODEL, help="模型ID")
    parser.add_argument("dir", nargs="?", default=DEFAULT_DIR, help="本地存储目录")
    parser.add_argument("--verify", action="store_true", help="仅校验模型完整性")
    
    args = parser.parse_args()
    
    if args.verify:
        print(f"校验模型: {args.model}")
        sys.exit(0 if verify_model(args.model, args.dir) else 1)
    else:
        download_model(args.model, args.dir)
