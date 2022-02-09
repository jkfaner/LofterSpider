#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 19:20
@Project:LoftSpider
@File:loginApi.py
@Desc:乐乎登录接口
"""
from API.baseApi import BaseLoftAPI


class LoginAPI(BaseLoftAPI):

    def loginAPI(self):
        """
        乐乎登录接口 须要POST请求
        :return:
        """
        url = "https://www.lofter.com/lpt/login.do"
        params = dict(product="lofter-pc",_=self.time())
        return self.join_url(url,params)

