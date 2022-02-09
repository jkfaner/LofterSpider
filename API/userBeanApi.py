#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 20:18
@Project:LofterSpider
@File:userBeanApi.py
@Desc:
"""
from API.baseApi import BaseLoftAPI


class UserBeanAPI(BaseLoftAPI):

    def getRecommendBlogListAPI(self):
        """
        获取推荐博客列表 接口
        :return:
        """
        url = "https://www.lofter.com/dwr/call/plaincall/UserBean.getRecommendBlogList.dwr"
        return url

    def getUserFollowingListAPI(self):
        """
        获取关注列表 接口
        :return:
        """
        url = "https://www.lofter.com/dwr/call/plaincall/UserBean.getUserFollowingList.dwr"
        return url


