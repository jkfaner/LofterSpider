#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/23 19:01
@Project:WeiboSpider
@File:jsonExtractorAPI.py
@Desc:json数据解析接口
"""
from Extractor.jsonDataFinder import JsonDataFinder


class ExtractorApi(object):
    """
    数据提取器接口
    """

    def finder(self, resp):
        finder = JsonDataFinder(resp)
        return finder

    def find_exists(self, resp, target: str) -> bool:
        """
        检查是否存在
        :return:
        """
        finder = self.finder(resp)
        exists = finder.find_first_path(target)
        if exists:
            return True
        return False

    def find_all_data(self, resp, target: str):
        """
        提取target下所有数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_data(target)
        if not target_list:
            return []
        if not isinstance(target_list, list):
            target_list = [target_list]
        return target_list

    def find_all_last_data(self, resp, target: str):
        """
        提取target下 的父级target值 或叫做 所有单个列表中最后一个target值
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_last_data(target)
        return target_list

    def find_first_data(self, resp, target: str):
        """
        提取target下第一个数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        first_target = finder.find_first_data(target)
        return first_target

    def find_last_data(self, resp, target: str):
        """
        提取target下第最后一个数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        first_target = finder.find_last_data(target)
        return first_target

    def find_assign_data(self, resp, target: str, index: int):
        """
        提取target下第index个数据
        :param resp:
        :param target:
        :param index:
        :return:
        """
        finder = self.finder(resp)
        assign_target = finder.find_assign_data(target, index)
        return assign_target

    def find_all_same_level_data(self, resp, target: str):
        """
        获得含有target的所有同级数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_same_level_data(target)
        return target_list

    def find_effective_data(self, resp, target: str):
        """
        获取有效数据
            eg.推特有效数据默认排除最后两个
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_data(target)
        return target_list[:-2]

    def split_all_data(self, resp, target: str):
        """
        分离所有target数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        return finder.split_all_data(target)

    def find_first_level_data(self,resp,target:str):
        """
        获取由内向外获取第一个出现的target的同级数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        return finder.find_first_level_data(target)

