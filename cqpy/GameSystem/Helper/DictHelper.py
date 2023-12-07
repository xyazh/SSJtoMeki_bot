class DictHelper:
    @staticmethod
    def wirteGet(d:dict,key,dis):
        r = dis
        if key in d:
            r = d[key]
        else:
            d[key] = dis
        return r