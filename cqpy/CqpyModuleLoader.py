import importlib.util
import os

class CqpyModuleLoader:
    def __init__(self,path="\\cqpy_plugin\\") -> None:
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        self.path = parent_directory+"\\SSJtoMeki_data"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.path += path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def getModulesPath(self) -> list[str]:
        items = os.listdir(self.path)
        subfolders = [item for item in items if os.path.isdir(os.path.join(self.path, item))]
        result = []
        for subfolder in subfolders:
            subfolder_path = os.path.join(self.path, subfolder)
            init_file_exists = os.path.isfile(os.path.join(subfolder_path, '__init__.py'))
            if init_file_exists:
                result.append(subfolder)
        return result
    
    def load(self):
        modules_path = self.getModulesPath()
        for package_path in modules_path:
            spec = importlib.util.spec_from_file_location('my_package', package_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            

