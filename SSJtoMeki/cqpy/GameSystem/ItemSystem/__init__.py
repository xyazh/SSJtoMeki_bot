import os,inspect
from . import Items
from .Items.BaseItem import BaseItem

def getFullClassesFormModul(o: object, filter=None, found_modules=None) -> list:
        r = []
        if found_modules == None:
            found_modules = set()
        if not hasattr(o, "__dict__"):
            return r
        for i in o.__dict__:
            if inspect.isclass(o.__dict__[i]):
                if inspect.isfunction(filter):
                    if not filter(o.__dict__[i]):
                        continue
                r.append(o.__dict__[i])
            elif inspect.ismodule(o.__dict__[i]):
                if o.__dict__[i] in found_modules:
                    continue
                found_modules.add(o.__dict__[i])
                r += getFullClassesFormModul(
                    o.__dict__[i], filter=filter, found_modules=found_modules)
        return r

__item_class_list = list(set(getFullClassesFormModul(Items,lambda clazz: issubclass(clazz, BaseItem))))
ITEMS_LIST = {}
for __item_class in __item_class_list:
    __item:BaseItem = __item_class()
    ITEMS_LIST[__item.name] = __item