import html

class RegisterData:
    def __init__(self,user_data:dict):
        self.user_name:str|None = None
        self.password:str|None = None
        self.user_mail:str|None = None
        self.check_code:str|None = None
        self.flag:bool = True
        if "user_name" in user_data:
            self.user_name = html.escape(user_data["user_name"])
        else:
            self.flag = False
        if "password" in user_data:
            self.password = user_data["password"]
        else:
            self.flag = False
        if "user_mail" in user_data:
            self.user_mail = user_data["user_mail"]
        else:
            self.flag = False
        if "check_number" in user_data:
            self.check_code = user_data["check_number"]
        else:
            self.flag = False

    def check(self)->bool:
        return (
            self.flag and 
            self.user_name and 
            self.password and 
            self.user_mail and 
            self.check_code and 
            type(self.user_name) == str and 
            type(self.password) == str and 
            type(self.user_mail) == str and 
            type(self.check_code) == str)

class LoggingData:
    def __init__(self,user_data:dict):
        self.password:str|None = None
        self.user_mail:str|None = None
        self.flag:bool = True
        if "password" in user_data:
            self.password = user_data["password"]
        else:
            self.flag = False

        if "user_mail" in user_data:
            self.user_mail = html.escape(user_data["user_mail"])
        else:
            self.flag = False

    def check(self)->bool:
        return (
            self.flag and 
            self.password and 
            self.user_mail and  
            type(self.password) == str and 
            type(self.user_mail) == str)