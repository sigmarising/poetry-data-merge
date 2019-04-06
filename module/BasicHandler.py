"""
class: BasicHandler
Author: Jason Zhang
Data: 2019/4/5
Desc:
    提供处理 国学大师数据集、八斗文学数据集 的 class 基类支持
"""
from abc import abstractmethod


class BasicHandler(object):
    def __init__(self, root_path: str, show_log: bool = False):
        """
        public: 构造函数
        :param root_path: 数据集路径
        :param show_log: 是否显示 log，默认为 不显示
        """
        self._root_path: str = root_path  # protected: 数据集根目录
        self._show_log: bool = show_log  # protected: 是否打印 log
        self.summary: dict = {
            "PoetsSum": 0,
            "PoemsSum": 0,
        }  # public: 对数据集进行汇总
        self.dynasties_summary: dict = {
            "元": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "先秦": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "南北朝": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "唐": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "宋": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "明": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "汉": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "清": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "辽": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "金": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "隋": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
            "魏晋": {
                "PoetsSum": 0,
                "PoemsSum": 0
            },
        }  # public: 对各个朝代进行汇总
        self.dynasties_poets: dict = {
            "元": [],
            "先秦": [],
            "南北朝": [],
            "唐": [],
            "宋": [],
            "明": [],
            "汉": [],
            "清": [],
            "辽": [],
            "金": [],
            "隋": [],
            "魏晋": [],
        }  # public: 对各个朝代的诗人进行统计 {Poet: str, PoemsSum: int}

    def _summary_add(self, dynasty: str, poet: str) -> None:
        """
        protected: 统计函数 传入新作品的朝代和作者 自动完成统计
        :param dynasty: 朝代
        :param poet: 作者
        :return: None
        """
        is_exist: bool = False
        for i in self.dynasties_poets[dynasty]:
            if i["Poet"] == poet:
                # 若诗人之前统计过
                i["PoemsSum"] += 1  # 诗人的作品数量 +1
                self.dynasties_summary[dynasty]["PoemsSum"] += 1  # 对应朝代的作品数量 +1
                self.summary["PoemsSum"] += 1  # 总体的作品数量 +1
                is_exist = True
                break
        if not is_exist:
            # 若诗人之前没有统计过
            self.dynasties_poets[dynasty].append({"Poet": poet, "PoemsSum": 1})  # 将其加入统计
            self.dynasties_summary[dynasty]["PoetsSum"] += 1  # 对应朝代的诗人数量 +1
            self.dynasties_summary[dynasty]["PoemsSum"] += 1  # 对应朝代的作品数量 +1
            self.summary["PoetsSum"] += 1  # 总体诗人数量 +1
            self.summary["PoemsSum"] += 1  # 总体作品数量 +1

    @abstractmethod
    def poems(self):
        pass
