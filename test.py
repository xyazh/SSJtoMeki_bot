import os

# 指定要检查的文件夹路径
folder_path = 'C:\\data\\cqpy\\SSJtoMeki_bot\\cqpy'

# 使用 os.listdir 获取文件夹中的所有项（包括文件和文件夹）
items = os.listdir(folder_path)

# 过滤出文件夹
subfolders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]

r = []
# 遍历每个子文件夹
for subfolder in subfolders:
    subfolder_path = os.path.join(folder_path, subfolder)
    init_file_exists = os.path.isfile(os.path.join(subfolder_path, '__init__.py'))

    #是的是的