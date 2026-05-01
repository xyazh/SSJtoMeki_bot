import time
import random
from pathlib import Path
from xyacqbot.datamanager.UserDataManager import UserDataManager
from xyacqbot.helper.RollHelper import RollHelper
from mods.LibModMCP.MCP import MCP

_MCP = MCP()


@_MCP.tool()
def sign(qq_id: int) -> str:
    """
    签到
    :param qq_id: 用户的qq号（5-11位的数字）
    :return: 签到信息
    """
    user = UserDataManager(qq_id)
    last_time = user.data.get("last_time", 0)
    if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
        return "%.2f秒前签到过，今日已签到" % (time.time()-last_time)
    n = user.data.get("n", 1)
    p = user.data.get("point", 1)
    ap = random.randint(int(n//2), n)
    ap = 1 if ap <= 0 else ap
    user.data["n"] = n+1
    user.data["point"] = p+ap
    user.data["last_time"] = time.time()
    return "第%d天签到获得：%dP" % (n, ap)


@_MCP.tool()
def jrrp(qq_id: int) -> str:
    """
    运势
    :param qq_id: 用户的qq号（5-11位的数字）
    :return: 运势信息
    """
    user = UserDataManager(qq_id)
    last_time = user.data.get("ys_last_time", 0)
    ys = -1
    if (last_time + 8 * 3600) // (24 * 3600) == (time.time() + 8 * 3600) // (24 * 3600):
        ys = user.data.get("ys", -1)
    flag = False
    if ys == -1:
        ys = RollHelper.presetSurpriseDistribution2()
        user.data["ys"] = ys
        user.data["ys_last_time"] = time.time()
        flag = True
    if ys <= 5:
        r = '大吉'
    elif ys <= 20:
        r = '吉'
    elif ys <= 35:
        r = '半吉'
    elif ys <= 50:
        r = '小吉'
    elif ys <= 65:
        r = '末小吉'
    elif ys <= 80:
        r = '末吉'
    elif ys <= 95:
        r = '凶'
    else:
        r = '大凶'
    if not flag:
        r += "，今天已经测过了"
    return "今日的幸运指数是%i %s" % (100-ys, r)


@_MCP.tool()
def point(qq_id: int) -> int:
    """
    查看当前点数
    :param qq_id: 用户的qq号（5-11位的数字）
    :return: 点数
    """
    user = UserDataManager(qq_id)
    return user.data.get("point", 1)

@_MCP.tool()
def foodList() -> str:
    """
    获取所有储存有食谱的食物列表
    :desc: 返回目前存有食谱的全部食物
    :return: 食谱列表
    """
    root_dir = Path('./data/dishes/')
    files_dict = {}
    for f in root_dir.rglob('*.md'):  # 只匹配 .md 文件
        if f.is_file():
            files_dict[f.stem] = str(f)
    return f"当前食物列表：{str(list(files_dict.keys()))}"

@_MCP.tool()
def howToCook(food_name: str) -> str:
    """
    获取已储存的指定食物的食谱
    :desc: 当用户问怎么做的时候，如果是foodList获取的食物，可以调用这个tool查询做法
    :param food_name: 食物名称
    :return: 食谱内容
    """
    root_dir = Path('./data/dishes/')
    files_dict = {}
    for f in root_dir.rglob('*.md'):  # 只匹配 .md 文件
        if f.is_file():
            files_dict[f.stem] = str(f)
    if food_name not in files_dict:
        return f"没有找到 {food_name} 的食谱"
    file_path = files_dict[food_name]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取 {food_name} 时出错: {e}"
    
@_MCP.tool()
def choiceFood() -> str:
    """
    随机获取一个食物
    :desc: 当用户问吃什么的时候，可以调用这个tool
    :return: 食物名称
    """
    root_dir = Path('./data/dishes/')
    files_dict = {}
    for f in root_dir.rglob('*.md'):  # 只匹配 .md 文件
        if f.is_file():
            files_dict[f.stem] = str(f)
    return random.choice(list(files_dict.keys()))