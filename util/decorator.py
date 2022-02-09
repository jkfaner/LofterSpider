#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/8 21:23
@Project:LofterSpider
@File:decorator.py
@Desc:装饰器
"""
import functools
import time


def desc_time(sleep_time):
    """
    休眠时间
    :param sleep_time: 时间
    :return:
    """

    def tracer(func):
        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            time.sleep(sleep_time)
            return func(self, *args, **kwargs)

        return new_func

    return tracer
