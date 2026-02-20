import json
import os
import weakref
import atexit
from ..xyazhServer.ConsoleMessage import ConsoleMessage

class DataManager:
    _instances = weakref.WeakValueDictionary()

    def __new__(cls, file_path=None):
        if file_path is None:
            file_path = os.path.join(os.getcwd(), 'data', 'data.json')
        file_path = os.path.abspath(file_path)

        instance = cls._instances.get(file_path)
        if instance is None:
            instance = super().__new__(cls)
            cls._instances[file_path] = instance
            instance._initFile(file_path)
            instance._load()
        return instance

    def __init__(self, file_path=None):
        if not hasattr(self, 'data'):
            self.data = {}

    def _initFile(self, file_path):
        self.file_path = file_path
        self.data_dir = os.path.dirname(file_path)

    def _load(self):
        os.makedirs(self.data_dir, exist_ok=True)
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        os.makedirs(self.data_dir, exist_ok=True)
        # 使用自定义序列化，剔除无法序列化的值
        def filterSerializable(obj):
            try:
                json.dumps(obj)
                return obj
            except (TypeError, OverflowError):
                ConsoleMessage.printWarning("无法序列化的数据：", obj)
                return None

        serializable_data = self._filterDict(self.data, filterSerializable)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)

    def _filterDict(self, obj, filter_func):
        """递归剔除不可序列化的数据"""
        if isinstance(obj, dict):
            return {k: self._filterDict(filter_func(v), filter_func) for k, v in obj.items() if filter_func(v) is not None}
        elif isinstance(obj, list):
            return [self._filterDict(filter_func(v), filter_func) for v in obj if filter_func(v) is not None]
        else:
            return obj

    def __del__(self):
        try:
            self.save()
        except Exception:
            pass

    @classmethod
    def _saveAll(cls):
        for instance in list(cls._instances.values()):
            try:
                instance.save()
            except Exception:
                pass

print(DataManager._instances)

# 程序退出时保存所有实例
atexit.register(DataManager._saveAll)
