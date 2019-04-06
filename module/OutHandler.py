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
    def __init__(self, root_path: str, threshold_cos: float, threshold_pre: float, show_log: bool = False):
        """
        public: 构造函数
        :param root_path: 数据集路径
        :param show_log: 是否显示 log，默认为 不显示
        """
        BasicHandler.__init__(self, root_path, show_log)  # 基类构造函数
        self.__threshold_cos = threshold_cos  # 余弦距离阈值
        self.__threshold_pre = threshold_pre  # 百分比阈值

    def poems(self):
        pass

    def insert(self, obj: dict) -> None:
        """
        public: 带去重的诗词插入
        :param obj: {dynasty, author, title, content, comment}
        :return: None
        """
        if self._show_log:
            s: str = "-".join((obj["dynasty"], obj["author"], obj["title"]))
            print(ColorLogDecorator.yellow("合并处理：" + s, "strong"))

        dynasty_path: str = os.path.join(self._root_path, obj["dynasty"])
        file_path: str = os.path.join(dynasty_path, obj["author"] + ".json")
        need_create_new_file: bool = False

        if not os.path.exists(dynasty_path):
            os.makedirs(dynasty_path)
            need_create_new_file = True

        if not os.path.exists(file_path):
            need_create_new_file = True

        if need_create_new_file:
            f = open(file_path, "w+", encoding="utf-8", errors="ignore")
            target: dict = {
                "dynasty": obj["dynasty"],
                "author": obj["author"],
                "poems": [{
                    "title": obj["title"],
                    "content": obj["content"],
                    "comment": obj["comment"]
                }]
            }
            json.dump(target, f, ensure_ascii=False, indent=4)
            f.close()
        else:
            f = open(file_path, "r", encoding="utf-8", errors="ignore")
            origin: dict = json.load(f)
            f.close()

            poems_list: list = origin["poems"]
            poems_same_name: list = []
            for item in poems_list:
                if item["title"] == obj["title"]:
                    poems_same_name.append(item)

            need_insert = True
            for item in poems_same_name:
                if self.__is_similarity(obj["content"], item["content"]):
                    need_insert = False
                    break

            if need_insert:
                origin["poems"].append(obj)
                f = open(file_path, "w+", encoding="utf-8", errors="ignore")
                json.dump(origin, f, ensure_ascii=False, indent=4)
                f.close()

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

        count: int = 0
        for char in content1:
            if content2.find(char) != -1:
                count += 1
        common_pre: float = count / len(content1)

        if self._show_log:
            s: str = "cos_num: " + str(cos_num) + " | common_pre: " + str(common_pre)
            print(ColorLogDecorator.yellow(s))

        if cos_num > self.__threshold_cos and common_pre > self.__threshold_pre:
            return True
        else:
            return False
