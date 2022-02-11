#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/9 18:00
@Project:LofterSpider
@File:spiderMiddleware.py
@Desc:爬虫中间件
"""
import json
from typing import List

from Extractor.entity.archive import Archive
from Extractor.entity.userBean import UserBean
from Session.spiderIter import SpiderIter


class SpiderMiddleware(SpiderIter):
    redis_user = "userBean"
    redis_archive = "archive"

    @staticmethod
    def entityToJson(entity):
        """
        entity模块中的对象转json
        :param entity:
        :return:
        """
        return json.dumps(entity, default=lambda entity: {
            k.split("__")[-1]: v
            for k, v in entity.__dict__.items()
        })

    @staticmethod
    def jsonToEntity(entity, json_str: str):
        """
        json转entity模块中的对象
        :param entity:
        :param json_str:
        :return:
        """
        _entity = entity()
        for k, v in json.loads(json_str).items():
            setattr(_entity, k, v)
        return _entity

    def get_followBlogUser(self, follow):
        """
        爬取关注用户信息
        :return:
        """
        blogId = int(follow.blogId)
        # 储存在redis数据库
        if not self.redisPool.redis.hexists(name=self.redis_user, key=blogId):
            self.redisPool.redis.hset(name=self.redis_user, key=blogId, value=self.entityToJson(follow))

    def get_userArchive(self, follow: UserBean, archives: List[Archive]):
        """
        爬取归档信息
        :param follow:
        :param kwargs:
        :return:
        """
        pass

    def get_permalinkPage(self, follow: UserBean, archive: Archive, index: int = None, total: int = None, get=False):
        """
        解析页面
        :param follow:用户对象
        :param archive:归档对象
        :param index:索引
        :param total:合计
        :param get:是否取数据
        :return:
        """
        key = "{}&{}".format(int(follow.blogId), archive.values.permalink)
        if self.redisPool.redis.hexists(name=self.redis_archive, key=key):
            return True if not get else self.redisPool.redis.hget(name=self.redis_archive, key=key)

        # archive_json = json.dumps(archive, default=lambda archive: {
        #     k.split("__")[-1]: v
        #     for k, v in archive.__dict__.items()
        # })
        archive_json = self.entityToJson(archive)
        self.redisPool.redis.hset(name=self.redis_archive, key=key, value=archive_json)
        return False if not get else archive_json
