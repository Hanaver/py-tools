import os
import zipfile
import rarfile
import time
def extract_archive(file_path, extract_dir):
    """
    解压缩压缩包到指定目录
    :param file_path: 压缩包文件路径
    :param extract_dir: 解压目标目录
    """
    # rarfile.UNRAR_TOOL = "C:/Program Files/WinRAR/UnRAR.exe"
    file_name = os.path.basename(file_path)
    print(file_name)
    if file_name.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"解压缩 '{file_name}' 到 '{extract_dir}'")
    elif file_name.endswith('.rar'):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(extract_dir)
            print(f"解压缩 '{file_name}' 到 '{extract_dir}'")
    else:
        print(f"不支持的压缩格式: {file_name}")

def extract_all_archives_in_directory(directory):
    """
    遍历目录下的所有文件，解压缩压缩包到当前目录
    :param directory: 目录路径
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            extract_archive(file_path, root)

# 指定要遍历的目录
directory_to_search = './files/'

# 解压缩目录下的所有压缩文件
extract_all_archives_in_directory(directory_to_search)

time.sleep(10)

print("执行成功")
