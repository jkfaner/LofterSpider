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

import requests

from API import LoftAPI
from Extractor.jsonExtractorAPI import ExtractorApi
from loftInit import LoftInit


class Login(LoftInit, LoftAPI, ExtractorApi):
    session = requests.Session()
    def __init__(self):
        self.login_time = 0
        self.cookies = None
        super(Login, self).__init__()

    @staticmethod
    def encryption(password):
        """
        乐乎密码加密
        :param password: 密码
        :return: sha256()加密的密码
        """
        import hashlib
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def __loginByAccount(self):
        """
        乐乎登录接口
        :return:
        """
        url = self.loginAPI()
        data = dict(
            phone=self.login_username,
            passport=self.encryption(self.login_password),
            type=0,
            clientType=0,
            deviceType=3,
            Target='www.lofter.com'
        )
        response_json = self.session.post(url=url, data=data).json()
        return response_json

    def checkLogin(self) -> bool:
        """
        检查登录cookies是否有效
        :return:
        """

        url = self.checkLoginAPI()
        headers = {"cookie": self.setCookie()}
        response_json = self.session.post(url=url, headers=headers).json()
        if self.find_first_data(response_json, "status") == 200:
            return True
        self.loginByAccount()
        return False

    def loginByAccount(self):
        """
        通过账号登录
        :return:
        """
        response_json = self.__loginByAccount()
        if self.find_first_data(response_json, "status") == 200:
            userid = self.find_first_data(response_json, "userid")
            deviceid = self.find_first_data(response_json, "deviceid")
            token = self.find_first_data(response_json, "token")
            sql = "SELECT username, token, deviceid from login"
            result = self.mysqlPool.getOne(sql=sql)

            if not result:
                sql = """INSERT INTO login(username,password,userid,deviceid,token) values (%s,%s,%s,%s,%s)"""
                self.mysqlPool.insert(sql=sql,
                                      param=[str(self.login_username),
                                             self.encryption(self.login_password),
                                             userid, deviceid, token]
                                      )
                self.mysqlPool.end()
            else:
                sql = "UPDATE login SET password=%s , userid=%s , deviceid=%s , token=%s WHERE username=%s"
                self.mysqlPool.update(sql=sql,
                                      param=[self.encryption(self.login_password),
                                             userid, deviceid, token,
                                             str(self.login_username)])
                self.mysqlPool.end()
            return True
        return False

    def login(self):
        """
        登录
        :return:
        """
        if not self.getCookiesByDB():
            if not self.loginByAccount():
                raise Exception("账号登录失败...")

        username, token, deviceid = self.getCookiesByDB()
        return username, token, deviceid

    def getCookiesByDB(self):
        """
        通过数据库获取cookies
        :return:
        """
        sql = "SELECT username, token, deviceid from login"
        result = self.mysqlPool.getOne(sql=sql)
        if result:
            username = str(result["username"], encoding="utf-8")
            token = str(result["token"], encoding="utf-8")
            deviceid = str(result["deviceid"], encoding="utf-8")
            return username, token, deviceid
        return result

    def setCookie(self):
        username, token, deviceid = self.login()
        cookies_item = {
            "LOFTER-PHONE-LOGINNUM": username,
            "LOFTER-PHONE-LOGIN-FLAG": 1,
            "phone": username,
            "LOFTER-PHONE-LOGIN-AUTH": token,
            "token": token,
            "deviceid": deviceid
        }
        cookies_list = ["{}={}".format(k, v) for k, v in cookies_item.items()]
        cookies = "; ".join(cookies_list)
        return cookies
