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
        s = s[1:-1]
        s = s.split(",")
        t = ""
        r = {}
        for i in s:
            if not t and "CQ:" in i:
                t = i.split(":")[1]
            if "=" in i:
                key_val = i.split("=",1)
                r[key_val[0]] = key_val[1]
        return t,r

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