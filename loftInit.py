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
from util.config import Config
from DateBase.mysqlDB import MyPymysqlPool


class LoftInit(object):

    def __init__(self):
        # 实例化配置文件对象
        self.global_config = Config()
        # 实例化数据库池
        self.mysqlPool = MyPymysqlPool(*self.__load_mysql())
        self.redisPool = Redis(*self.__load_redis())
        self.login_username, self.login_password = self.__load_login()
        self.open_thread,self.thread_num = self.__load_spider()

    def __load_spider(self)->tuple:
        """
        加载爬虫配置信息
        :return:
        """
        try:
            open_thread = self.global_config.getBoolean("spider", "open_thread")
        except ValueError:
            raise Exception("是否开启多线程下载，True or False")
        try:
            thread_num = self.global_config.getInt("spider", "thread_num")
        except ValueError:
            raise Exception("线程数仅允许为整数")
        return open_thread,thread_num

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

    def __load_redis(self) -> tuple:
        """
        加载redis数据库配置信息
        :return:
        """
        host = self.global_config.get("redis", "host")
        port = self.global_config.getInt("redis", "port")
        password = self.global_config.get("redis", "password")
        db = self.global_config.getInt("redis", "db")
        return host, port, password, db

    def __load_login(self) -> tuple:
        """
        加载登录配置信息
        :return:
        """
        username = self.global_config.getInt("login", "username")
        password = self.global_config.get("login", "password")
        return username, password
