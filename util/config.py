#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/1/31 19:31
@Project:LofterSpider
@File:config.py
@Desc:配置信息加载
"""
import os
import configparser


class Config(object):
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')
        self._configRaw = configparser.RawConfigParser()
        self._configRaw.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)

    def getRaw(self, section, name):
        return self._configRaw.get(section, name)

    def getInt(self, section, name):
        return self._configRaw.getint(section, name)

    def getFolat(self, section, name):
        return self._configRaw.getfloat(section, name)

    def getBoolean(self, section, name):
        return self._configRaw.getboolean(section, name)

