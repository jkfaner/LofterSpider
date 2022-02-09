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
import requests

from API import LoftAPI


class SessionMiddleware(LoftAPI):
    cookies = None

    def __init__(self, username, token, deviceid):
        # 实例化session
        self.session = requests.Session()
        super(SessionMiddleware, self).__init__()
        self.username = username
        self.token = token
        self.deviceid = deviceid

    def fetch(self, url, headers=None, method='post', **kwargs):
        if method.lower() == 'post':
            headers.update({"cookie": self.setCookie()})
        return super(SessionMiddleware, self).fetch(url, headers, method, session=self.session, **kwargs)

    def setCookie(self):
        if not self.cookies:
            cookies_item = {
                "LOFTER-PHONE-LOGINNUM": self.username,
                "LOFTER-PHONE-LOGIN-FLAG": 1,
                "phone": self.username,
                "LOFTER-PHONE-LOGIN-AUTH": self.token,
                "token": self.token,
                "deviceid": self.deviceid
            }
            cookies_list = ["{}={}".format(k, v) for k, v in cookies_item.items()]
            self.cookies = "; ".join(cookies_list)
        return self.cookies
