#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/1 08:57
@Project:LofterSpider
@File:dwrToJson.py
@Desc:dwr js 数据转 json
"""
import copy
import json
import re


class DWRToJson(object):
    notes = "//"

    def __init__(self, dwr: str):
        assert dwr, "dwr没有数据"
        # 删除开头注释信息
        dwr_split = self.remove_note(dwr.replace("\r",""))
        # 获取需要提取的有效键
        new_dwr_split, self.keys = self.getValidKeys(dwr_split)
        # 获取dwr键元素
        element_obj = self.getElement(new_dwr_split)
        # 提取dwr值数
        element_obj = self.extractor(dwr_split=new_dwr_split, element_obj=element_obj)
        self.dwr_info = self.assign(element_obj)

    def getJson(self):
        """
        获取json数据
        :return:
        """
        dwr_dict = self.getDict()
        dwr_json = json.dumps(dwr_dict)
        return dwr_json

    def getDict(self):
        """
        获取字典数据
        :return:
        """
        __dwr_json = json.dumps({k: self.dwr_info[k] for k in self.keys})
        dwr_dict = json.loads(__dwr_json)
        return dwr_dict

    def getValidKeys(self, dwr_split: list):
        """
        获取需要提取的有效键
        :param dwr_split:
        :return:
        """
        _dwr_split = list()
        keys = None
        for _ in dwr_split[::-1]:
            if _.startswith("dwr"):
                keys = re.findall("s\d+", _)
            else:
                _dwr_split.insert(0, _)
        return _dwr_split, keys

    def assign(self, element_obj):
        """
        数据赋值
        :param element_obj:
        :return:
        """
        _element_obj = copy.deepcopy(element_obj)
        if isinstance(_element_obj, dict):
            for k, v in _element_obj.items():
                if isinstance(v, list):
                    for n, _ in enumerate(v):
                        if _ in element_obj:
                            del element_obj[k][n]
                            element_obj[k].insert(n, element_obj[_])

        if isinstance(_element_obj, dict):
            for k, v in _element_obj.items():
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        if vv in element_obj:
                            element_obj[k][kk] = element_obj[vv]
                        else:
                            element_obj[k][kk] = vv
        return element_obj

    def change_value(self, str):
        if str == "null":
            return None
        elif str == "false":
            return False
        elif str == "true":
            return True
        elif str:
            return self.replace_str(str)

    @staticmethod
    def strip_tags(html):
        """
        Python中过滤HTML标签的函数
        :param html:
        :return:
        """
        # 删除含有html标签的Unicode编码字符串
        pattern = re.compile(r'<[^>]+>', re.U)
        result = pattern.sub('', html)
        return result

    @staticmethod
    def strip_quotationMark(s: str):
        """
        删除字符串引号
        :param s:
        :return:
        """
        if s.startswith('"'):
            begin = s.find('"') + 1
            end = s.rfind('"')
            return s[begin:end]
        return s

    @staticmethod
    def strip_unicode(s: str):
        """
        清除含有unicode编码的字符串
        :param s:
        :return:
        """
        if '\\' in s:
            # 英文，中文，日文，韩文
            # epre = re.compile(r"[\s\w]+")
            chre = re.compile(u".*[\u4E00-\u9FA5]+.*")
            # jpre = re.compile(u".*[\u3040-\u30FF\u31F0-\u31FF]+.*")
            # hgre = re.compile(u".*[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF]+.*")
            new_s = chre.sub('', s).encode('utf-8').decode('unicode_escape')
            # new_s = eval(repr(s).replace("\\\\", "\\"))
            return new_s
        return s

    @staticmethod
    def strip_html(s: str):
        """
        去除HTML
        :param s:
        :return:
        """
        # 删除含有html标签的Unicode编码字符串
        pattern = re.compile(r'<[^>]+>', re.U)
        result = pattern.sub('', s)
        return result

    def replace_str(self, s):
        """
        替换字符串
        :param s:
        :return:
        """
        # 清除双引号
        s = self.strip_quotationMark(s)
        # 清除html标签
        s = self.strip_html(s)
        # unicode编码
        s = self.strip_unicode(s)
        # emoji unicode编码
        # s = self.strip_emoji_unicode(s)
        return s

    def remove_note(self, dwr: str):
        """
        去除注释信息
            前两行是注释
        :param dwr:
        :return:
        """
        dwr_split = dwr.split("\n")
        for _ in dwr.split("\n"):
            if _.startswith(self.notes):
                dwr_split.remove(_)

        new_dwr_split = list()
        for _ in "\n".join(dwr_split).split(";\n"):
            if _.startswith("var"):
                for j in _.split(";"):
                    new_dwr_split.append(j)
            elif _.startswith("dwr"):
                new_dwr_split.append(_)
            else:
                for i in _.split(";s"):
                    if not i.startswith("s") and not i.startswith("\n"):
                        new_dwr_split.append("s{}".format(i))
                    else:
                        new_dwr_split.append(i.replace("\n", ""))
        return new_dwr_split

    def getElement(self, dwr_split: list):
        """
        提取dwr键元素
        :param dwr_split:
        :return:
        """
        __element = dict()
        var_dict = re.findall("var (s\d+)=\{\}", ''.join(dwr_split))
        var_list = re.findall("var (s\d+)=\[\]", ''.join(dwr_split))
        for _dict in var_dict:
            __element[_dict] = dict()
        for _list in var_list:
            __element[_list] = list()
        return __element

    def extractor(self, dwr_split: list, element_obj: dict):
        """
        提取dwr数据
        :param dwr_split:
        :return:
        """
        for new_dwr in dwr_split:
            values_dict = re.findall('([\s\w]+)\.([\s\w]+)=(.+)', new_dwr)
            values_list = re.findall('([\s\w]+)\[([\d]+)\]=([\s\w]+)', new_dwr)
            if values_dict:
                element = values_dict[0][0]
                key = values_dict[0][1]
                value = self.change_value(values_dict[0][2])
                # print(element,key,value)
                element_obj[element][key] = value
            if values_list:
                element = values_list[0][0]
                key = int(values_list[0][1])
                value = self.change_value(values_list[0][2])
                element_obj[element].insert(key, value)
        return element_obj


if __name__ == '__main__':
    with open("/Users/llb/PycharmProjects/LoftSpider/Extractor/dwr.txt", "r") as f:
        dwr = f.read()
    d = DWRToJson(dwr)
    print(d.getJson())
