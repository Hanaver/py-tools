import os
import shutil

# 源目录，要从中搜索特定文件夹
# default_source_dir = "/software/"
# default_target_dir = "/temp/"

source_dir = "/software/"
# 目标目录，要将找到的文件夹复制到此处
target_dir = "/temp/"
# 要查找的文件夹名（假设是完全匹配）
folder_name_to_find = input("请输入文件夹名称:")

def search_and_copy(source, target, folder_name):
    counter = 1
    for root, dirs, files in os.walk(source):
        for dir_name in dirs:
            if dir_name == folder_name:
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
    
    print('执行成功')

# 调用函数开始搜索和复制操作
search_and_copy(source_dir, target_dir, folder_name_to_find)