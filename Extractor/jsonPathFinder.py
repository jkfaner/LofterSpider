#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 18:58
@Project:WeiboSpider
@File:jsonPathFinder.py
@Desc:json数据路径查找
"""
import json
from typing import List


class JsonPathFinder:

    def __init__(self, json_str, mode='key'):
        if isinstance(json_str, dict) or isinstance(json_str, list):
            self.data = json_str
        elif isinstance(json_str, str):
            self.data = json.loads(json_str)
        else:
            raise Exception(f"数据类型错误, The type is {type(json_str)}-->{json_str}")
        self.mode = mode

    def iter_node(self, rows, road_step, target):
        if isinstance(rows, dict):
            key_value_iter = (x for x in rows.items())
        elif isinstance(rows, list):
            key_value_iter = (x for x in enumerate(rows))
        else:
            return
        for key, value in key_value_iter:
            current_path = road_step.copy()
            current_path.append(key)
            if self.mode == 'key':
                check = key
            else:
                check = value
            if check == target:
                yield current_path
            if isinstance(value, (dict, list)):
                yield from self.iter_node(value, current_path, target)

    def find_data(self, target_path: list):
        """
        通过路径查找数据
        :param target_path:
        :return: 值
        """
        if not target_path:
            return []
        if isinstance(target_path[0], list):
            new_data = list()
            for targets in target_path:
                data = self.data
                for target in targets:
                    data = data[target]
                new_data.append(data)
            if len(new_data) == 1:
                return new_data[0]
            return new_data

        data = self.data
        for target in target_path:
            data = data[target]
        return data

    def find_sameLeaveData(self, target_path: list):
        """
        通过路径查找同级数据
        :param target_path:
        :return:
        """
        if not target_path:
            return []
        if isinstance(target_path[0], list):
            new_data = list()
            for targets in target_path:
                data = self.data
                target_length = len(targets)
                for target_index in range(target_length - 1):
                    data = data[targets[target_index]]
                new_data.append(data)
            return new_data

        data = self.data
        target_length = len(target_path)
        for target_index in range(target_length - 1):
            data = data[target_path[target_index]]
        return data

    def del_data(self, target_path: List[list], data):
        """
        通过路径删除数据
        :param target_path:
        :return:
        """
        if not target_path:
            return False
        if isinstance(target_path[0], list):
            for targets in target_path:
                for n, target in enumerate(targets):
                    if n + 1 == len(target_path):
                        del data[target]
                    else:
                        data = data[target]
        else:
            for n, target in enumerate(target_path):
                if n + 1 == len(target_path):
                    del data[target]
                else:
                    data = data[target]

    def find_first_path(self, target: str) -> list:
        """
        获取第一个路径
        :param target:
        :return:
        """
        path_iter = self.iter_node(self.data, [], target)
        for path in path_iter:
            return path
        return []

    def find_last_path(self, target: str) -> list:
        """
        获取最后一个路径
        :param target:
        :return:
        """
        path_iter = self.iter_node(self.data, [], target)
        if path_iter:
            new_path_iter = list(path_iter)
            if new_path_iter:
                return new_path_iter[-1]
        return []

    def find_all_path(self, target) -> List[list]:
        """
        获取所有路径
        :param target:
        :return:
        """
        path_iter = self.iter_node(self.data, [], target)
        return list(path_iter)
