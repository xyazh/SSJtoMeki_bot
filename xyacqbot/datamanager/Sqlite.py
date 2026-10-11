import os
import sqlite3
import weakref
import threading
import atexit


class DataManager:
    _instances = weakref.WeakValueDictionary()
    _global_lock = threading.RLock()

    def __new__(cls, file_path=None):
        if file_path is None:
            file_path = os.path.join(os.getcwd(), "data", "data.db")
        file_path = os.path.abspath(file_path)
        with cls._global_lock:
            instance = cls._instances.get(file_path)
            if instance is None:
                instance = super().__new__(cls)
                cls._instances[file_path] = instance
                instance._load(file_path)
            return instance

    def __init__(self, file_path=None):
        pass

    def _load(self, file_path):
        self.file_path = file_path
        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )
        self.conn = sqlite3.connect(
            file_path,
            check_same_thread=False
        )
        self.lock = threading.RLock()
        self._closed = False

    def execute(self, sql, params=()):
        with self.lock:
            return self.conn.execute(sql, params)

    def executemany(self, sql, params):
        with self.lock:
            return self.conn.executemany(sql, params)

    def query(self, sql, params=()):
        with self.lock:
            cursor = self.conn.execute(sql, params)
            return cursor.fetchall()

    def queryOne(self, sql, params=()):
        with self.lock:
            cursor = self.conn.execute(sql, params)
            return cursor.fetchone()

    def commit(self):
        with self.lock:
            if not self._closed:
                self.conn.commit()

    def rollback(self):
        with self.lock:
            if not self._closed:
                self.conn.rollback()

    def close(self):
        with self.lock:
            if self._closed:
                return
            try:
                self.conn.commit()
            finally:
                self.conn.close()
                self._closed = True
                self._instances.pop(
                    self.file_path,
                    None
                )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    @classmethod
    def _saveAll(cls):
        for instance in list(cls._instances.values()):
            try:
                instance.close()
            except Exception:
                pass


atexit.register(DataManager._saveAll)