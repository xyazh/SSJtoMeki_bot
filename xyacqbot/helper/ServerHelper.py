import inspect

class ServerHelper:
    @staticmethod
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
                r += ServerHelper.getFullClassesFormModul(
                    o.__dict__[i], filter=filter, found_modules=found_modules)
        return r

    @staticmethod
    def checkFunsArgs(fuc: object, args: list | tuple) -> bool:
        sign = inspect.signature(fuc)
        try:
            sign.bind(*args)
        except TypeError:
            return False
        return True