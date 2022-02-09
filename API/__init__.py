#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 19:14
@Project:LoftSpider
@File:__init__.py.py
@Desc:
"""
from API.archiveBeanApi import ArchiveBeanAPI
from API.loginApi import LoginAPI
from API.userBeanApi import UserBeanAPI
from Session.fetch import Session


class LoftAPI(Session, LoginAPI, UserBeanAPI, ArchiveBeanAPI):

    def getPageAPI(self, blogName: str, permalink: str) -> str:
        url = "https://{}.lofter.com/post/{}".format(blogName, permalink)
        return url
