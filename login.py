#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 19:20
@Project:LoftSpider
@File:login.py
@Desc:乐乎登录
"""
from API import LoftAPI
from DateBase.mysqlDB import MyPymysqlPool
from Extractor.jsonExtractorAPI import ExtractorApi


class Login(LoftAPI,ExtractorApi):

    def __init__(self, username, password, mysqlPool: MyPymysqlPool):
        super(Login, self).__init__()
        self.username, self.password = username, self.encryption(password)
        self.mysqlPool = mysqlPool

    @staticmethod
    def encryption(password):
        """
        乐乎密码加密
        :param password: 密码
        :return: sha256()加密的密码
        """
        import hashlib
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def loginByAccount(self):
        """
        乐乎登录接口
        :return:
        """
        url = self.loginAPI()
        data = dict(
            phone=self.username,
            passport=self.password,
            type=0,
            clientType=0,
            deviceType=3,
            Target='www.lofter.com'
        )
        response_json = self.fetch_json(url=url, data=data, method="post")
        return response_json

    def login(self):
        """
        登录
        :return:
        """
        sql = "SELECT username, token, deviceid from login"
        result = self.mysqlPool.getOne(sql=sql)
        if not result:
            response_json = self.loginByAccount()
            if self.find_first_data(response_json, "status") == 200:
                userid = self.find_first_data(response_json, "userid")
                deviceid = self.find_first_data(response_json, "deviceid")
                token = self.find_first_data(response_json, "token")
                sql = """INSERT INTO login(username,password,userid,deviceid,token) values (%s,%s,%s,%s,%s)"""
                self.mysqlPool.insert(sql=sql, param=[str(self.username), self.password, userid, deviceid, token])
                self.mysqlPool.end()
                return self.login()
        username = str(result["username"], encoding="utf-8")
        token = str(result["token"], encoding="utf-8")
        deviceid = str(result["deviceid"], encoding="utf-8")
        return username, token, deviceid
