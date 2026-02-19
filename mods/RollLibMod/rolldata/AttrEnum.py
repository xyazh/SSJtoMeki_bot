from enum import Enum, EnumMeta


class AttrEnumMeta(EnumMeta):
    @classmethod
    def _missing_(cls, value):
        raise NotImplementedError()

    def __getitem__(cls, item):
        return cls._missing_(item)


class AttrEnum(Enum, metaclass=AttrEnumMeta):
    STR = (20, "STR", "str", "Strength", "力量")
    CON = (20, "CON", "con", "Constitution", "体质")
    SIZ = (20, "SIZ", "siz", "Size", "体型")
    DEX = (20, "DEX", "dex", "Dexterity", "敏捷")
    APP = (20, "APP", "app", "Appearance", "外貌", "外表")
    INT = (20, "INT", "int", "Intelligence", "智力", "灵感")
    POW = (20, "POW", "pow", "Power", "意志")
    EDU = (20, "EDU", "edu", "Education", "教育")
    LUK = (20, "LUK", "luk", "Luck", "幸运", "运气")
    HP = (4, "HP", "hp", "Hit Points", "生命值", "生命", "血量")
    MP = (4, "MP", "mp", "Magic Points", "魔法值", "魔法", "法力")
    SAN = (20, "SAN", "san", "SAN值", "san值", "Sanity", "理智值", "理智")
    MOV = (8, "MOV", "Move Rate", "移动率", "移动力", "行动力")
    ACCOUNTING = (5, "Accounting", "会计")
    ANTHROPOLOGY = (1, "Anthropology", "人类学")
    APPRAISE = (5, "Appraise", "估价")
    ARCHAEOLOGY = (1, "Archaeology", "考古学")
    ART = (5, "Art", "艺术", "技艺")
    CHARM = (15, "Charm", "魅惑", "取悦")
    CLIMB = (20, "Climb", "攀爬")
    COMPUTER_USE = (5, "Computer use", "计算机", "计算机使用")
    CREDIT_RATING = (0, "Credit Rating", "信用评级")
    CTHULHU_MYTHOS = (0, "Cthulhu Mythos", "CM", "cm", "克苏鲁神话")
    DISGUISE = (5, "Disguise", "乔装")
    DODGE = (40, "Dodge", "闪避")
    DRIVE_AUTO = (20, "Drive Auto", "汽车驾驶")
    ELECTRICAL_REPAIR = (10, "Electrical Repair", "电气维修")
    ELECTRONICS = (1, "Electronics", "电子", "电子学")
    FAST_TALK = (5, "Fast Talk", "话术")
    FIGHT = (25, "Fighting", "格斗")
    FIREARMS = (20, "Firearms", "射击")
    FIRST_AID = (30, "First Aid", "急救")
    HISTORY = (5, "History", "历史")
    INTIMIDATE = (15, "Intimidate", "恐吓")
    JUMP = (20, "Jump", "跳跃")
    LANGUAGE = (55, "Language", "语言", "外语")
    LAW = (5, "Law", "法律")
    LIBRARY_USE = (20, "Library Use", "图书馆使用")
    LISTEN = (20, "Listen", "聆听")
    LOCKSMITH = (1, "Locksmith", "开锁", "锁匠")
    MECHANICAL_REPAIR = (10, "Mechanical Repair", "机械维修")
    MEDICINE = (1, "Medicine", "医学")
    NATURAL_WORLD = (10, "Natural World", "博物学")
    NAVIGATE = (10, "Navigate", "导航")
    OCCULT = (5, "Occult", "神秘学")
    OPERATE_HEAVY_MACHINES = (
        1, "Operate Heavy Machines", "重型机械操作", "操作重型机械", "重机")
    PERSUADE = (10, "Persuade", "说服")
    PILOT = (1, "Pilot", " 驾驶")
    PSYCHOANALYSIS = (1, "Psychanalysis", "精神分析")
    PSYCHOLOGY = (10, "Psychology", "心理学")
    RIDE = (5, "Ride", "骑术")
    SCIENCE = (1, "Science", "科学")
    SLEIGHT_OF_HAND = (10, "Sleight of Hand", "巧手", "妙手")
    SPOT_HIDDEN = (25, "Spot Hidden", "侦查", "侦察")
    STEALTH = (20, "Stealth", "潜行")
    SURVIVAL = (10, "Survival", "生存")
    SWIM = (20, "Swim", "游泳")
    THROW = (20, "Throw", "投掷")
    TRACK = (10, "Track", "追踪")
    BEAST_TRAINING = (5, "Beast Training", "驯兽")
    DIVING = (1, "Diving", "潜水")
    DEMOLITIONS = (1, "Demolitions", "爆破")
    READ_LIP = (1, "Read Lip", "读唇")
    HYPNOSIS = (1, "Hypnosis", "催眠")
    ARTILLERY = (1, "Artillery", "炮术")
    KNOWLEDGE = (1, "Knowledge", "学识")

    def __init__(self, dis_val, *args):
        self.dis_val = dis_val
        self.names: tuple[str] = args

    def __eq__(self, other):
        if isinstance(other, AttrEnum):
            return self.names == other.names
        return other in self.names

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def normalizeAlias(value) -> str:
        return str(value).strip().casefold()

    @classmethod
    def aliasMap(cls) -> dict[str, "AttrEnum"]:
        alias_map: dict[str, AttrEnum] = {}
        for member in cls:
            for alias in member.names:
                alias_map[cls.normalizeAlias(alias)] = member
        return alias_map

    @classmethod
    def _missing_(cls, value):
        return cls.aliasMap().get(cls.normalizeAlias(value))


if __name__ == "__main__":
    print(AttrEnum["STR"])
