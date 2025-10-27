from typing import List, Optional, Union, Literal, Dict, Any

class Container:
    def __init__(self,name:str, obj: object,t: Literal["moudle","object","class"]):
        self.obj = obj
        self.t:Literal["moudle","object","class"] = t
        self.name = name