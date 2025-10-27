import sys
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Dict
from ..xyazhServer.ConsoleMessage import ConsoleMessage

class ModLoader:
    def __init__(self, mods_root: str):
        self.mods_root = Path(mods_root).resolve()
        self.loaded_mods: Dict[str, ModuleType] = {}

    def loadMod(self, mod_dir: Path) -> ModuleType:
        """
        用包名导入单个模块，保证 main.py 内部相对导入可以正常工作
        """
        main_path = mod_dir / "main.py"
        if not main_path.exists():
            raise FileNotFoundError(f"{main_path} 不存在")
        mod_name = mod_dir.name  # 包名使用文件夹名
        # 插入 mods 根目录到 sys.path，使 Python 能识别包
        mods_root = str(mod_dir.parent.resolve())
        if mods_root not in sys.path:
            sys.path.insert(0, mods_root)
        # 导入包下的 main 模块
        full_module_name = f"{mod_name}.main"  # 如 TestMod.main
        mod = importlib.import_module(full_module_name)
        # 注册到 loaded_mods
        self.loaded_mods[mod_name] = mod
        ConsoleMessage.printC(f"加载模块 {mod_name}")
        return mod

    def loadAll(self):
        """
        扫描 mods_root 文件夹下所有模块并加载
        """
        for mod_dir in self.mods_root.iterdir():
            if mod_dir.is_dir() and (mod_dir / "main.py").exists():
                self.loadMod(mod_dir)

    def reloadMod(self, mod_name: str) -> ModuleType:
        """
        重新加载已加载模块
        """
        if mod_name not in self.loaded_mods:
            raise KeyError(f"模块 {mod_name} 未加载")
        mod = self.loaded_mods[mod_name]
        reloaded = importlib.reload(mod)
        self.loaded_mods[mod_name] = reloaded
        return reloaded

    def unloadMod(self, mod_name: str):
        """
        卸载模块
        """
        if mod_name in self.loaded_mods:
            del sys.modules[mod_name]
            del self.loaded_mods[mod_name]

    def getMod(self, mod_name: str) -> ModuleType:
        """
        获取已加载的模块对象
        """
        return self.loaded_mods.get(mod_name)
    
    def getMods(self) -> Dict[str, ModuleType]:
        """
        获取所有已加载的模块对象
        """
        return self.loaded_mods
