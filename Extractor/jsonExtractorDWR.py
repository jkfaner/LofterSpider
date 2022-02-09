#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 11:51
@Project:LofterSpider
@File:jsonExtractorDWR.py
@Desc:
"""
from Extractor.dwrToJson import DWRToJson


class ExtractorDWRAPI(object):

    def getDict(self, dwr):
        dwr_obj = DWRToJson(dwr=dwr)
        return dwr_obj.getDict()

    def getJson(self,dwr):
        dwr_obj = DWRToJson(dwr=dwr)
        return dwr_obj.getJson()
