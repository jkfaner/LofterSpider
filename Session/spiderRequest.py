#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 23:40
@Project:LofterSpider
@File:spiderRequest.py
@Desc:爬虫
"""
from requests import Response
import random
from Session.sessionMiddleware import SessionMiddleware


class SessionRequest(SessionMiddleware):

    @staticmethod
    def random_nums(num=6):
        """
        随机数字串
        :param num:
        :return:
        """
        str = ""
        for i in range(num):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        return str

    def getUserFollowingList(self, nums: int = 1000, order_by_follow: bool = True) -> Response:
        """
        获取关注列表数据
        :param nums: 爬取数量
        :param order_by_follow: 最近互动 false 最近关注 true
        :return:
        """
        url = self.getUserFollowingListAPI()
        data = {
            "callCount": 1,
            "scriptSessionId": "${scriptSessionId}187",
            "httpSessionId": "",
            "c0-scriptName": "UserBean",
            "c0-methodName": "getUserFollowingList",
            "c0-id": 0,
            "c0-param0": "number:%s" % nums,
            "c0-param1": "number:0",
            "c0-param2": "boolean:%s" % "true" if order_by_follow else "false",  # 最近互动 false 最近关注 true
            "batchId": self.random_nums()  # 随机值 可以固定
        }
        headers = dict(referer="https://www.lofter.com/follow")
        response = self.fetch(url=url, data=data, headers=headers)
        return response

    def getUserArchiveList(self, blogName: str, blogId: int, timestamp: int, nums=50):
        """
        获取用户归档数据
        :param blogName:
        :param blogId:
        :param timestamp:
        :param nums:
        :return:
        """
        url = self.getArchivePostByTimeApi(blogName)
        data = {
            "callCount": 1,
            "scriptSessionId": "${scriptSessionId}187",
            "httpSessionId": '',
            "c0-scriptName": "ArchiveBean",
            "c0-methodName": "getArchivePostByTime",
            "c0-id": 0,
            "c0-param0": "boolean:false",
            "c0-param1": "number:%d" % blogId,
            "c0-param2": "number:%d" % timestamp,
            "c0-param3": "number:%d" % nums,
            "c0-param4": "boolean:false",
            "batchId": self.random_nums()  # 随机值 可以固定
        }
        headers = dict(origin="https://%s.lofter.com" % blogName,
                       referer="https://%s.lofter.com/view" % blogName)
        response = self.fetch(url=url, data=data, headers=headers)
        return response

    def getHtmlPage(self, blogName: str, permalink: str):
        """
        获取页面
        :param blogName:
        :param permalink:
        :return:
        """
        url = self.getPageAPI(blogName=blogName, permalink=permalink)
        headers = dict(referer="https://%s.lofter.com/view" % blogName)
        response = self.fetch(url=url, method="get", headers=headers)
        return response
