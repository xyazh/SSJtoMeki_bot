import html

class MsgData:
    def __init__(self,user_data:dict):
        self.title:str|None = None
        self.text:str|None = None
        self.token:str|None = None
        self.name:str|None = None
        self.flag:bool = True
        if "title" in user_data:
            self.title = html.escape(user_data["title"])
        else:
            self.flag = False
        if "text" in user_data:
            self.text = html.escape(user_data["text"])
        else:
            self.flag = False
        if "token" in user_data:
            self.token = user_data["token"]
        if "name" in user_data:
            self.name = html.escape(user_data["name"])


    def check(self)->bool:
        if self.flag:
            if len(self.title)>60:
                return False
            if len(self.text)>2000:
                return False
        if not (self.token or self.name):
            return False
        if self.token:
            if type(self.token) != str:
                return
        if self.name:
            if type(self.name) != str:
                return  
        return (
            self.flag and 
            self.title and 
            self.text and 
            type(self.title) == str and 
            type(self.text) == str)