from .Tree import Tree
from .UrlHelper import UrlHelper
import os
import urllib.parse


class PageManager:
    D = "*"

    def __init__(self):
        self.path_trees = {
            "GET": Tree(),
            "POST": Tree()
        }

    def addPath(self,path: str, fuc: object, t: str):
        path = path.replace("\\", "/")
        h_dir = UrlHelper.pathSplit(path)
        if not t in self.path_trees:
            self.path_trees[t] = Tree()
        in_node = self.path_trees[t]
        for i in h_dir:
            if i == "":
                in_node.leaf = fuc
                break
            elif i in in_node.child_nodes:
                in_node = in_node.child_nodes[i]
            else:
                new_node = Tree()
                new_node.parent_node = in_node
                new_node.val = i
                in_node.child_nodes[i] = new_node
                in_node = new_node

    def findPath(self,path: str, t: str) -> object | None:
        h_dir = UrlHelper.pathSplit(path)
        if not t in self.path_trees:
            return None
        in_node = self.path_trees[t]
        r = None
        for i in h_dir:
            if i == "":
                r = in_node.leaf
                break
            elif i in in_node.child_nodes:
                in_node = in_node.child_nodes[i]
            elif self.D in in_node.child_nodes:
                in_node = in_node.child_nodes[self.D]
            else:
                break
        return r

    def register(self,path: str, t: str = "GET"):
        def r(fuc):
            self.addPath(path, fuc, t)
            return fuc
        return r

    def addFileTree(self,root: str, virtual_root: str, fuc: object, t: str = "GET"):
        for dirpath, dirnames, filenames in os.walk(root):
            dirpath = dirpath.replace(root, virtual_root, 1)
            for filename in filenames:
                path = dirpath+"/"+filename
                self.addPath(path, fuc, t)
