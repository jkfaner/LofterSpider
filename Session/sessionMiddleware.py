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


class SessionMiddleware(Login):


    def fetch(self, url, headers=None, method='post', **kwargs):
        if method.lower() == 'post':
            self.checkLogin()
            headers.update({"cookie": self.setCookie()})

        return super(SessionMiddleware, self).fetch(url=url, headers=headers, method=method, **kwargs)
