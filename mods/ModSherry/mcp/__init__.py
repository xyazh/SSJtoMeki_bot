import time
import random
import uuid
import base64
import hashlib
import string
import datetime
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
def randomInt(min_val: int, max_val: int) -> int:
    """
    生成指定范围的随机整数
    :param min_val: 最小值
    :param max_val: 最大值
    :return: 随机整数
    """
    return random.randint(min_val, max_val)


@_MCP.tool()
def randomFloat(min_val: float, max_val: float) -> float:
    """
    生成指定范围的随机浮点数
    :param min_val: 最小值
    :param max_val: 最大值
    :return: 随机浮点数
    """
    return random.uniform(min_val, max_val)


@_MCP.tool()
def randomUuid() -> str:
    """
    生成一个随机 UUID
    :return: UUID 字符串
    """
    return str(uuid.uuid4())


@_MCP.tool()
def textMd5(text: str) -> str:
    """
    计算文本的 MD5 值
    :param text: 输入文本
    :return: MD5 字符串
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


@_MCP.tool()
def textSha256(text: str) -> str:
    """
    计算文本的 SHA256 值
    :param text: 输入文本
    :return: SHA256 字符串
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@_MCP.tool()
def textBase64Encode(text: str) -> str:
    """
    将文本进行 Base64 编码
    :param text: 输入文本
    :return: Base64 编码后的字符串
    """
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


@_MCP.tool()
def textBase64Decode(encoded: str) -> str:
    """
    将 Base64 编码文本解码回原文
    :param encoded: Base64 字符串
    :return: 解码后的文本
    """
    return base64.b64decode(encoded.encode("utf-8")).decode("utf-8")


@_MCP.tool()
def randomChoice(options: list[object]) -> object:
    """
    从列表中随机选择一个元素
    :param options: 列表
    :return: 随机选中的元素
    """
    if not options:
        return None
    return random.choice(options)


@_MCP.tool()
def randomSample(options: list, k: int) -> list:
    """
    从列表中随机选择 k 个不重复的元素
    :param options: 列表
    :param k: 选择数量
    :return: 随机选出的元素列表
    """
    return random.sample(options, min(k, len(options)))


@_MCP.tool()
def generatePassword(length: int = 12) -> str:
    """
    生成随机密码
    :param length: 密码长度（默认12位）
    :return: 随机密码字符串
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))


@_MCP.tool()
def randomColor() -> str:
    """
    生成一个随机的十六进制颜色
    :return: 例如 "#3fa9f5"
    """
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


@_MCP.tool()
def currentTimestamp() -> int:
    """获取当前时间戳"""
    return int(time.time())

@_MCP.tool()
def formatTime(timestamp: int = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间"""
    ts = timestamp or int(time.time())
    return datetime.datetime.fromtimestamp(ts).strftime(fmt)


@_MCP.tool()
def foodList() -> list[str]:
    """
    获取所有储存有食谱的食物列表
    :return: 食谱列表
    """
    root_dir = Path('./data/dishes/')
    files_dict = {}
    for f in root_dir.rglob('*.md'):  # 只匹配 .md 文件
        if f.is_file():
            files_dict[f.stem] = str(f)
    return list(files_dict.keys())

@_MCP.tool()
def howToCook(food_name: str) -> str:
    """
    获取已储存的指定食物的食谱
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