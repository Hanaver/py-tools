import os
import shutil
import re
import time

"""
循环source目录的所有文件夹，并一文件夹名称在target目录下循环模糊匹配，匹配上即将文件夹copy到source目录的当前目录下
"""

# 源目录，要从中搜索特定文件夹
# default_source_dir = "/software/"
# default_target_dir = "/temp/"

source_dir = "./source"
# 目标目录，要将找到的文件夹复制到此处
target_dir = "./target"
# 要查找的文件夹名（假设是完全匹配）
# folder_name_to_find = input("请输入文件夹名称:")

def search_and_copy(source, target, folder_name):
    counter = 1
    for root, dirs, files in os.walk(source):
        for dir_name in dirs:
            if re.search('.*'+folder_name+'.*', dir_name):
                source_subfolder = os.path.join(root, dir_name)
                base_target_subfolder = os.path.join(target, dir_name)
                target_subfolder = base_target_subfolder

                # 判断文件是否存在
                while os.path.exists(target_subfolder):
                    # 重命名新复制的文件夹以避免冲突
                    target_subfolder = f"{base_target_subfolder}_{counter}"
                    counter += 1    
            
                # 复制找到的文件夹到目标目录
                shutil.copytree(source_subfolder, target_subfolder)
    

for root, dirs, files in os.walk(source_dir):
    for dir_name in dirs:
        # 调用函数开始搜索和复制操作
        search_and_copy(target_dir, os.path.join(root), dir_name)

print('执行成功')
time.sleep(10)
