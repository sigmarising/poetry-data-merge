"""
class: BdHandler
Author: Jason Zhang
Date: 2019/4/6
Desc:
    用于处理八斗文学数据集
    使用生成器获取诗词
"""
import json
import os
import re
from .BasicHandler import BasicHandler
from .ColorLogDecorator import ColorLogDecorator


class BdHandler(BasicHandler):
    def __init__(self, root_path: str, show_log: bool = False):
        """
        public: 构造函数
        :param root_path: 数据集路径
        :param show_log: 是否显示 log，默认为 不显示
        """
        BasicHandler.__init__(self, root_path, show_log)
        self.__r1 = re.compile(r"（[^）]*）|【[^】]*】|\([^\)]*\)|\[[^\]]*\]")  # 用于分离正文中的括号

    def poems(self):
        """
        public: 生成器 返回数据集中每一首诗
        :return: None
        """
        for dynasty in os.listdir(self._root_path):  # 朝代

            dynasty_path: str = os.path.join(self._root_path, dynasty)
            for poet_file in os.listdir(dynasty_path):  # 作者

                poet_file_path: str = os.path.join(dynasty_path, poet_file)
                with open(poet_file_path, 'r', encoding='utf-8', errors='ignore') as f:  # 每一个文件
                    text_raw: dict = json.load(f)
                    text_target: dict = {
                        "dynasty": dynasty.strip(),
                        "author": text_raw["poet"].strip(),
                        "title": "",
                        "content": "",
                        "comment": "",
                    }  # yield 的内容

                    if self._show_log:
                        s: str = "-".join((text_target["dynasty"], text_target["author"]))
                        print(ColorLogDecorator.blue("正在处理-八斗文学：" + s))


                    for item in text_raw["poem"]:  # 每首诗
                        content: str = item["content"].strip()
                        content = "".join(self.__r1.split(content))

                        if content.strip() == "":
                            continue

                        text_target["title"] = item["title"].strip()
                        text_target["content"] = content.strip()
                        text_target["comment"] = item["comment"].strip()

                        self._summary_add(text_target["dynasty"], text_target["author"])
                        yield text_target
