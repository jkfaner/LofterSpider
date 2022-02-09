#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 19:28
@Project:LofterSpider
@File:loftInit.py
@Desc:
"""
from DateBase.redisDB import Redis
from Extractor.jsonExtractorAPI import ExtractorApi
from Extractor.jsonExtractorDWR import ExtractorDWRAPI
from login import Login
from Session.spiderIter import SpiderIter
from util.config import Config
from DateBase.mysqlDB import MyPymysqlPool


class LoftInit(object):

    def __init__(self):
        # 实例化配置文件对象
        self.global_config = Config()
        # 实例化数据库池
        __mysqlPool = MyPymysqlPool(*self.__load_mysql())
        self.redisPool = Redis(*self.__load_redis())
        # 实例化登录
        __loginObj = Login(*self.__load_login(), mysqlPool=__mysqlPool)
        # 实例化爬虫接口
        self.spiderObj = SpiderIter(*__loginObj.login())

    def __load_mysql(self) -> tuple:
        """
        加载数据库信息
        :return:
        """
        host = self.global_config.get("mysql", "host")
        port = self.global_config.getInt("mysql", "port")
        user = self.global_config.get("mysql", "user")
        pwd = self.global_config.get("mysql", "pwd")
        db_name = self.global_config.get("mysql", "db_name")
        return host, port, user, pwd, db_name

    def __load_redis(self)->tuple:
        """
        加载redis数据库配置信息
        :return:
        """
        host = self.global_config.get("redis", "host")
        port = self.global_config.getInt("redis", "port")
        password = self.global_config.get("redis", "password")
        db = self.global_config.getInt("redis", "db")
        return host,port,password,db

    def __load_login(self) -> tuple:
        """
        加载登录配置信息
        :return:
        """
        username = self.global_config.getInt("login", "username")
        password = self.global_config.get("login", "password")
        return username, password
