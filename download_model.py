#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从魔塔社区(ModelScope)下载模型的脚本,支持断点续传和完整性校验"""

import os
import sys
from modelscope import snapshot_download
from modelscope.hub.api import HubApi

def verify_model(model_id, local_dir):
    """
    校验模型文件完整性

    Args:
        model_id: 模型ID
        local_dir: 本地存储目录

    Returns:
        bool: 是否完整
    """
    try:
        # 获取模型的远程文件列表
        api = HubApi()
        model_files = api.get_model_files(model_id)

        print("正在校验模型文件...")

        # 使用原始路径: models/okwinds/Qwen3-xxx
        model_dir = os.path.join(local_dir, model_id)

        if not os.path.exists(model_dir):
            print(f"未找到模型目录: {model_dir}")
            return False

        print(f"检查目录: {model_dir}")

        # 统计文件数量
        total_files = len(model_files)
        print(f"需要校验 {total_files} 个文件")

        # 检查每个必需的文件是否存在
        for i, file_info in enumerate(model_files, 1):
            file_path = os.path.join(model_dir, file_info['Path'])
            if not os.path.exists(file_path):
                print(f"[{i}/{total_files}] 缺失文件: {file_info['Path']}")
                return False

            # 检查文件大小
            local_size = os.path.getsize(file_path)
            remote_size = file_info.get('Size', 0)
            if remote_size > 0 and local_size != remote_size:
                print(f"[{i}/{total_files}] 文件大小不匹配: {file_info['Path']}")
                print(f"  本地大小: {local_size} 字节, 远程大小: {remote_size} 字节")
                return False

        print(f"所有 {total_files} 个文件校验通过")
        return True
    except Exception as e:
        print(f"校验失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def download_model(model_id, local_dir="./models", verify=True):
    """
    从ModelScope下载模型,支持断点续传

    Args:
        model_id: 模型ID,例如 "qwen/Qwen3-0.6B"
        local_dir: 本地存储目录,默认为 "./models"
        verify: 是否在下载后校验完整性

    Returns:
        str: 模型存储路径
    """
    os.makedirs(local_dir, exist_ok=True)
    print(f"开始下载模型: {model_id}")
    print(f"存储路径: {local_dir}\n")

    model_path = snapshot_download(model_id, cache_dir=local_dir)
    print(f"\n模型下载完成: {model_path}")

    # 校验模型完整性
    if verify:
        if verify_model(model_id, local_dir):
            print("✓ 模型下载完整")
        else:
            print("✗ 模型可能不完整,建议重新下载")
            return None

    return model_path

if __name__ == "__main__":
    # 解析命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        # 仅校验模式
        model_id = sys.argv[2] if len(sys.argv) > 2 else "qwen/Qwen3-0.6B"
        local_dir = sys.argv[3] if len(sys.argv) > 3 else "./models"

        print(f"校验模型: {model_id}")
        if verify_model(model_id, local_dir):
            print("✓ 模型完整")
            sys.exit(0)
        else:
            print("✗ 模型不完整")
            sys.exit(1)
    else:
        # 下载模式
        model_id = sys.argv[1] if len(sys.argv) > 1 else "qwen/Qwen3-0.6B"
        local_dir = sys.argv[2] if len(sys.argv) > 2 else "./models"

        download_model(model_id, local_dir)
