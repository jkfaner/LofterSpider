#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 11:33
@Project:LofterSpider
@File:blogBeanApi.py
@Desc:
"""
from API.baseApi import BaseLoftAPI


class BlogBean(BaseLoftAPI):

    def getBlogStatNew(self):
        """
        获取博客状态新
        :return:
        """
        url = "https://www.lofter.com/dwr/call/plaincall/BlogBean.getBlogStatNew.dwr"
        return url

    def getResembleBlog(self):
        """
        获取相似博客
        :return:
        """
        url = "https://www.lofter.com/dwr/call/plaincall/BlogBean.getResembleBlog.dwr"
        return url