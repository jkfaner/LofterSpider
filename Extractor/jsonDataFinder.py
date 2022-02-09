#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 18:59
@Project:WeiboSpider
@File:jsonDataFinder.py
@Desc:json数据查找
"""
from copy import deepcopy

from Extractor.jsonPathFinder import JsonPathFinder


class JsonDataFinder(JsonPathFinder):

    def find_first_data(self, target: str):
        """
        获得第一条数据
        :param target:
        :return:
        """
        target_path = self.find_first_path(target)
        return self.find_data(target_path)

    def find_last_data(self, target: str):
        """
        获得第一条数据
        :param target:
        :return:
        """
        target_path = self.find_last_path(target)
        return self.find_data(target_path)

    def find_assign_data(self, target: str, index: int):
        """
        获取指定索引的数据
        :param target:
        :param index:
        :return:
        """
        target_path = self.find_first_path(target)
        target_path.append(index)
        return self.find_data(target_path)

    def find_all_data(self, target: str):
        """
        获得所有数据
        :param target:
        :return:
        """
        target_path = self.find_all_path(target)
        return self.find_data(target_path)

    def find_all_last_data(self, target: str):
        """
        提取target下 的父级target值 或叫做 所有单个列表中最后一个target值
        :param target:
        :return:
        """
        target_path = self.find_all_path(target)
        _target_path = [i for i in target_path if len(i) == 2]
        return self.find_data(_target_path)

    def find_all_same_level_data(self, target: str):
        """
        获得含有target的同级数据
        :param target:
        :return:
        """
        target_path = self.find_all_path(target)
        new_target_path = [path[:-1] for path in target_path]
        return self.find_data(new_target_path)

    def split_all_data(self, target: str):
        """
        分离所有target数据
            删除某key-value键值对
        :param target:
        :return:
        """
        data = deepcopy(self.data)
        for path in self.find_all_path(target=target):
            self.del_data(path, data)
        return data

    def find_first_level_data(self,target:str):
        """
        获取由内向外获取第一个出现的target的同级数据
        :param resp:
        :param target:
        :return:
        """
        target_path = self.find_all_path(target)
        if not target_path:
            return []
        first_len = len(target_path[0])
        first_level_path = [_ for _ in target_path if len(_) == first_len]
        return self.find_sameLeaveData(first_level_path)