import os
import json
import io
import logging


class DataManager:
    def __init__(self, path="\\cqpy_data\\"):
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        self.path = parent_directory+"\\SSJtoMeki_data"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.path += path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def getFileIO(self, file_name: str, type: str = "rb") -> io.IOBase:
        full_path = self.path + file_name
        if os.path.exists(full_path):
            f = open(full_path, type)
            return f
        return None

    def openFile(self, path: str, mode: str, *args, **kw) -> io.IOBase:
        f = open(self.getFileFullPath(path, create=False), mode, *args, **kw)
        return f

    def getFileFullPath(self, file_name: str, create: bool = True) -> str:
        full_path = self.path + file_name
        if not os.path.exists(full_path) and create:
            with open(full_path, "wb") as f:
                f.write(json.dumps({}, ensure_ascii=False,
                        indent=4).encode("utf8"))

        return full_path

    def hasFile(self, file_name: str) -> bool:
        full_path = self.path + file_name
        return os.path.exists(full_path)

    def craftFile(self, file_name: str, dis_data: dict = {}) -> None:
        full_path = self.path + file_name
        with open(full_path, "wb") as f:
            f.write(json.dumps(dis_data, ensure_ascii=False,
                    indent=4).encode("utf8"))

    def get(self, file_name: str, key: str = None) -> dict | list | int | str | float | bool | None:
        j = None
        try:
            with open(self.getFileFullPath(file_name), "rb") as f:
                j = json.loads(f.read())
        except BaseException as e:
            logging.exception(e)
        if j != None:
            if key == None:
                return j
            if isinstance(j, dict) and key in j:
                return j[key]
        return None

    def findGet(self, file_name: str, key: str = None, dis_val=None):
        r = self.get(file_name, key)
        if r == None:
            return dis_val
        return r

    def set(self, file_name: str, key: str, val: dict | list | int | str | float | bool) -> bool:
        j = None
        try:
            with open(self.getFileFullPath(file_name), "rb") as f:
                j: dict = json.loads(f.read())
        except BaseException as e:
            logging.exception(e)
        if j != None:
            if isinstance(j, dict):
                j[key] = val
                try:
                    with open(self.getFileFullPath(file_name), "wb") as f:
                        f.write(json.dumps(j, ensure_ascii=False,
                                indent=4).encode("utf8"))
                    return True
                except BaseException as e:
                    logging.exception(e)
        return False

    def getMenbers(self, file_name: str, keys: None | list[str] | tuple[str] = None, dis_fnl: object = lambda x: None) -> dict:
        j = None
        r = {}
        try:
            with open(self.getFileFullPath(file_name), "rb") as f:
                j = json.loads(f.read())
        except BaseException as e:
            logging.exception(e)
        if j != None:
            if not isinstance(keys, list) and not isinstance(keys, tuple):
                return r
            for i in keys:
                if i in j:
                    r[i] = j[i]
                else:
                    r[i] = dis_fnl(i)
        return r

    def setMenbers(self, file_name: str, key_vals: dict) -> bool:
        j = None
        try:
            with open(self.getFileFullPath(file_name), "rb") as f:
                j: dict = json.loads(f.read())
        except BaseException as e:
            logging.exception(e)
        if j != None:
            if isinstance(j, dict):
                for key in key_vals:
                    j[key] = key_vals[key]
                try:
                    with open(self.getFileFullPath(file_name), "wb") as f:
                        f.write(json.dumps(j, ensure_ascii=False,
                                indent=4).encode("utf8"))
                    return True
                except BaseException as e:
                    logging.exception(e)
        return False
