from .DataLoader import DataLoader
import random
class I18n:
    data_loader = DataLoader()

    @staticmethod
    def format(key:str)->str:
        lang_data = I18n.data_loader.lang_data
        s = lang_data.get(key,key)
        if isinstance(s,list):
            s = random.choice(s)
        return str(s)
    
    @staticmethod
    def formatRaw(key:str):
        lang_data = I18n.data_loader.lang_data
        s = lang_data.get(key,key)
        return s