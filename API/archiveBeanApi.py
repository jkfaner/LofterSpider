#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 13:27
@Project:LofterSpider
@File:archiveBeanApi.py
@Desc:
"""
from API.baseApi import BaseLoftAPI


class ArchiveBeanAPI(BaseLoftAPI):

    def getArchivePostByTimeApi(self, blogName: str):
        """
        获取归档信息
        :param blogName:
        :return:
        """
        url = "https://%s.lofter.com/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr"
        return url % blogName
