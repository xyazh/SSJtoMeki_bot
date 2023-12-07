ROLL_LIKE_ARRS_TABLE = {
    "hp": ["hp","生命","生命值","hit point","血量"],
    "mp": ["mp","魔力","法力","魔法","魔力值","法力值","魔法值","magic point"],
    "san": ["san","理智","sanity"],
    "str": ["str","力量"],
    "dex": ["dex","敏捷"],
    "con": ["con","体质"],
    "siz": ["siz","体型"],
    "app": ["app","外貌"],
    "int": ["int","智力","灵感","智力灵感"],
    "pow": ["pow","意志"],
    "edu": ["edu","教育","知识","教育知识"],
    "luk": ["luk","luck","幸运","运气"],
    "会计": ["会计","mp魔法hp体力会计"],
    "信用": ["信用","信誉","信用评级"],
    "克苏鲁": ["克苏鲁","克苏鲁神话","cm"],
    "图书馆": ["图书馆","图书馆使用"]
}
ROLL_LIKE_ARRS_LIST = {j:i for i in ROLL_LIKE_ARRS_TABLE for j in ROLL_LIKE_ARRS_TABLE[i]}

class RollDict(dict):
    def __setitem__(self, __key, __value) -> None:
        if __key in ROLL_LIKE_ARRS_LIST:
            __like_key = ROLL_LIKE_ARRS_LIST[__key]
            for __i in ROLL_LIKE_ARRS_TABLE[__like_key]:
                super().__setitem__(__i, __value)
        else:
            super().__setitem__(__key, __value)

if __name__ == "__main__":
    d = RollDict({})
    d["生命值"] = 1
    print(d)