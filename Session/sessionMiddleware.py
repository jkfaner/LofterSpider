#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/1 14:53
@Project:LofterSpider
@File:sessionMiddleware.py
@Desc:session中间件
"""

from login import Login
import time

class SessionMiddleware(Login):


    def fetch(self, url, headers=None, method='post', **kwargs):
        if method.lower() == 'post':
            self.checkLogin()
            headers.update({"cookie": self.setCookie()})
            time.sleep(2)

        return super(SessionMiddleware, self).fetch(url=url, headers=headers, method=method, **kwargs)
