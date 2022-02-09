#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 20:26
@Project:LofterSpider
@File:userBean.py
@Desc:
'''


class UserBean(object):

    def __init__(self):
        self.__blogId = None
        self.__blogInfo = None
        self.__followTime = None
        self.__follower = None
        self.__hotCount = None
        self.__id = None
        self.__lastPublishTime = None
        self.__lastVisitTime = None
        self.__responseCount = None
        self.__score = None
        self.__specialFollow = None
        self.__userId = None

    @property
    def blogId(self):
        return self.__blogId

    @blogId.setter
    def blogId(self, blogId):
        self.__blogId = blogId

    @property
    def blogInfo(self):
        return self.__blogInfo

    @blogInfo.setter
    def blogInfo(self, blogInfo):
        self.__blogInfo = blogInfo

    @property
    def followTime(self):
        return self.__followTime

    @followTime.setter
    def followTime(self, followTime):
        self.__followTime = followTime

    @property
    def follower(self):
        return self.__follower

    @follower.setter
    def follower(self, follower):
        self.__follower = follower

    @property
    def hotCount(self):
        return self.__hotCount

    @hotCount.setter
    def hotCount(self, hotCount):
        self.__hotCount = hotCount

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def lastPublishTime(self):
        return self.__lastPublishTime

    @lastPublishTime.setter
    def lastPublishTime(self, lastPublishTime):
        self.__lastPublishTime = lastPublishTime

    @property
    def lastVisitTime(self):
        return self.__lastVisitTime

    @lastVisitTime.setter
    def lastVisitTime(self, lastVisitTime):
        self.__lastVisitTime = lastVisitTime

    @property
    def responseCount(self):
        return self.__responseCount

    @responseCount.setter
    def responseCount(self, responseCount):
        self.__responseCount = responseCount

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        self.__score = score

    @property
    def specialFollow(self):
        return self.__specialFollow

    @specialFollow.setter
    def specialFollow(self, specialFollow):
        self.__specialFollow = specialFollow

    @property
    def userId(self):
        return self.__userId

    @userId.setter
    def userId(self, userId):
        self.__userId = userId
