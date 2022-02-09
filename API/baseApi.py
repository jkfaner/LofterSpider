#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 19:15
@Project:LoftSpider
@File:baseApi.py
@Desc:接口基类
"""
import time
from urllib.parse import urlencode


class BaseLoftAPI(object):

    @staticmethod
    def join_url(url, params):
        """
        合并url
        :param url:url
        :param params:参数
        :return:
        """
        url = url + "?" + urlencode(params)
        return url

    def time(self):
        return int(time.time()*1000)
