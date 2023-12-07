import json,re
from .xyazhServer.ConsoleMessage import ConsoleMessage

class CQCode:
    def __init__(self,t:str,data:dict):
        self.t = t
        self.data = data

class CQCodeHelper:
    @staticmethod
    def countCQ(s:str)->list[str]:
        count = False
        r = []
        a_cq = []
        for i in s:
            if i == "[":
                count = True
            if count:
                a_cq.append(i)
            if i == "]":
                count = False
                r.append("".join(a_cq))
                a_cq = []
        return r
            
    @staticmethod
    def parseCQ(s:str)->tuple[str,dict]|None:
        s = re.sub(r"(\{.*\})",lambda m:m.group()
        .replace(",","|xcqescape114")
        .replace(":","|xcqescape514")
        .replace("[","|xcqescape191")
        .replace("]","|xcqescape919")
        .replace("=","|xcqescape810")
        .replace("\'","|xcqescape853")
        .replace("\"","|xcqescape641"),s)
        s = (s
            .replace("[","[\"CQType=")
            .replace("]","\"]")
            .replace(",","\",\""))
        try:
            l:list[str] = json.loads(s)
            r = {}
            for i in l:
                ls = i.split("=",1)
                r[ls[0]] = ls[1]
            d = {}
        except BaseException as e:
            ConsoleMessage.printWarning("无效的CQ码：" + str(e))
            return None
        for i in r:
            r[i] = (r[i]
                .replace("|xcqescape114",",")
                .replace("|xcqescape514",":")
                .replace("|xcqescape191","[")
                .replace("|xcqescape919","]")
                .replace("|xcqescape810","=")
                .replace("|xcqescape853","\'")
                .replace("|xcqescape641","\""))
            d[i] = r[i]
        t_str = d.pop("CQType")
        t_str = t_str[3:]
        return (t_str,d)

    @staticmethod
    def creatCQCodeFromMsg(msg:str)->list[CQCode]:
        cq_strs = CQCodeHelper.countCQ(msg)
        r = []
        for i in cq_strs:
            t = CQCodeHelper.creatCQCodeFromCQCodeStr(i)
            if t != None:
                r.append(t)
        return r

    @staticmethod
    def creatCQCodeFromCQCodeStr(cqcode:str)->CQCode|None:
        t = CQCodeHelper.parseCQ(cqcode)
        if t == None:
            return None
        return CQCode(*t)
    
    @staticmethod
    def creatCQCodeFromData(t:str,data:dict)->CQCode:
        return CQCode(t,data)