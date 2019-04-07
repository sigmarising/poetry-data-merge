"""
class: OutHandler
Author: Jason Zhang
Date: 2019/4/6
Desc:
    用于操作合并后的数据集
"""
import json
import os
import numpy as np
from .BasicHandler import BasicHandler
from .ColorLogDecorator import ColorLogDecorator


class OutHandler(BasicHandler):
    def __init__(self, root_path: str, threshold_cos: float, output_cos: bool, show_log: bool = False):
        """
        public: 构造函数
        :param root_path: 数据集路径
        :param show_log: 是否显示 log，默认为 不显示
        """
        BasicHandler.__init__(self, root_path, show_log)  # 基类构造函数
        self.__threshold_cos = threshold_cos  # 余弦距离阈值
        self.__output_cos = output_cos  # 是否输出余弦值到文件中
        self.__file_cos = os.path.join(self._root_path, "cos_value.txt")
        self.__cache = {
            "dynasty": "",
            "author": "",
            "poems": []
        }  # 对于同一个 朝代-诗人 的内存缓存

        if self.__output_cos:
            if not os.path.exists(self._root_path):
                os.makedirs(self._root_path)
            with open(self.__file_cos, "w+", encoding="utf-8", errors="ignore") as f:
                f.write("The Cos Value Summary:\n")

    def poems(self):
        pass

    def insert(self, obj: dict) -> None:
        """
        public: 带去重的诗词插入
        :param obj: {dynasty, author, title, content, comment, flush}
        :return: None
        """
        dynasty_path: str = os.path.join(self._root_path, obj["dynasty"])
        file_path: str = os.path.join(dynasty_path, obj["author"] + ".json")

        if self.__cache["dynasty"] == obj["dynasty"] and self.__cache["author"] == obj["author"]:
            # 可以使用缓存操作
            pass
        else:
            # 缓存未名中 需初始化操作
            if not os.path.exists(dynasty_path):  # 若朝代目录不存在 则创建
                os.makedirs(dynasty_path)

            if os.path.exists(file_path):  # 若作者json存在 则读取并初始化缓存
                origin: dict
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    origin = json.load(f)
                self.__cache = {
                    "dynasty": origin["dynasty"],
                    "author": origin["author"],
                    "poems": origin["poems"]
                }
            else:  # 否则 只初始化缓存的朝代作者
                self.__cache = {
                    "dynasty": obj["dynasty"],
                    "author": obj["author"],
                    "poems": []
                }

        need_insert: bool = True
        for item in self.__cache["poems"]:
            if self.__is_similarity(obj["title"], item["title"]):  # 首先比较标题相似性
                if self.__is_similarity(obj["content"], item["content"]):
                    # 发现相似文档 进行文档丰富性对比处理
                    if len(item["title"]) < len(obj["title"]):
                        item["title"] = obj["title"]
                    if len(item["content"]) < len(obj["content"]):
                        item["content"] = obj["content"]
                    if obj["comment"] != "":
                        item["comment"] = " | ".join((item["comment"], obj["comment"]))

                    need_insert = False
                    break
            else:
                continue

        if need_insert:
            self.__cache["poems"].append({
                "title": obj["title"],
                "content": obj["content"],
                "comment": obj["comment"]
            })

        if obj["flush"]:
            with open(file_path, "w+", encoding="utf-8", errors="ignore") as f:
                json.dump(self.__cache, f, ensure_ascii=False, indent=4)
            self.__clear_cache()

    def __is_similarity(self, content1: str, content2: str) -> bool:
        """
        private: 用于判断两个文本是否是相似的
        :param content1: 文本1
        :param content2: 文本2
        :return:
            True 相似
            False 不相似
        """
        space: list = list(set([x for x in content1 + content2]))
        c1: list = []
        c2: list = []
        for char in space:
            c1.append(content1.count(char))
            c2.append(content2.count(char))
        v1 = np.array(c1)
        v2 = np.array(c2)
        v1 = v1 / v1.max()
        v2 = v2 / v2.max()
        cos_num: float = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

        if self.__output_cos:
            with open(self.__file_cos, "a", encoding="utf-8", errors="ignore") as f:
                f.write("text1: " + content1 + "\n")
                f.write("text2: " + content2 + "\n")
                f.write(str(cos_num) + "\n")

        result: bool
        if cos_num > self.__threshold_cos:
            result = True
        else:
            result = False

        if self._show_log:
            s1: str = ColorLogDecorator.blue("  cos value: " + str(cos_num))
            s2: str = ColorLogDecorator.green(" True ", "bg") if result else ColorLogDecorator.red(" False ", "bg")
            print(s1 + " " + s2)

        return result

    def __clear_cache(self) -> None:
        """
        private: 清除缓存
        :return: None
        """
        self.__cache = {
            "dynasty": "",
            "author": "",
            "poems": []
        }
