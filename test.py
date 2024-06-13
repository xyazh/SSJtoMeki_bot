import re

pattern = r"^(gal_news|gal新闻|galgame新闻|gal资讯|galgame资讯|旮旯|gal|galgame)$"
order = "gal"

print(re.fullmatch(pattern, order) is not None)

"""r = []
# 遍历每个子文件夹
for subfolder in subfolders:
    subfolder_path = os.path.join(folder_path, subfolder)
    init_file_exists = os.path.isfile(os.path.join(subfolder_path, '__init__.py'))

    #是的是的
"""