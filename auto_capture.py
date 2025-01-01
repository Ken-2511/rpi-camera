#!/usr/bin/env python3
import time
import os
import shutil
from datetime import datetime, timedelta
from picamera2 import Picamera2

def ensure_dir(directory):
    """如果目录不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def cleanup_old_folders(base_path, days=15):
    """
    删除 base_path 下所有“YYYY-MM-DD”形式的文件夹，
    如果其日期早于当前日期 days 天，就整文件夹删除
    """
    now = datetime.now()
    cutoff_date = now.date() - timedelta(days=days)

    if not os.path.isdir(base_path):
        return

    for entry in os.scandir(base_path):
        # 仅处理文件夹，并且名字类似 YYYY-MM-DD
        if entry.is_dir():
            folder_name = entry.name  # 例如 "2025-01-01"
            # 判断文件夹名是否形如 "YYYY-MM-DD"
            # 同时要兼容可能存在一些其他杂乱目录
            # 这里做一个简易的判断 + 日期转换
            try:
                folder_date = datetime.strptime(folder_name, "%Y-%m-%d").date()
            except ValueError:
                # 如果不能转换，说明不是有效的日期文件夹，跳过
                continue

            # 判断是否早于 cutoff_date
            if folder_date < cutoff_date:
                folder_path = os.path.join(base_path, folder_name)
                print(f"Deleting old folder: {folder_path}")
                shutil.rmtree(folder_path)

def main():
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration()
    picam2.start()

    base_path = "/home/ken/Documents/cameraCap"
    print("Camera started. Begin loop for auto capturing...")

    while True:
        now = datetime.now()
        second = now.second

        # 判断秒是否为 0 或 30
        if second == 0 or second == 30:
            # 先清理旧文件夹（15天前的）
            cleanup_old_folders(base_path, days=15)

            # 构造日期和时间
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H-%M-%S")
            
            # 目录: /home/ken/Documents/cameraCap/2025-01-01
            date_directory = os.path.join(base_path, date_str)
            ensure_dir(date_directory)

            # 文件: /home/ken/Documents/cameraCap/2025-01-01/13-05-00.jpg
            filename = os.path.join(date_directory, f"{time_str}.jpg")

            # 短暂休眠让相机曝光/白平衡更稳定（可根据需要微调时间）
            time.sleep(0.5)

            # 拍照
            picam2.switch_mode_and_capture_file(capture_config, filename)
            print(f"Captured: {filename}")

            # 避免 0.5 秒后仍在同一个秒点触发，sleep多一点
            time.sleep(2)
        else:
            # 如果还没到 0/30 秒，0.5 秒后再看
            time.sleep(0.5)

if __name__ == "__main__":
    main()
