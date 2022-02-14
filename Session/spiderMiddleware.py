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
    redis_view = "view"

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

    def get_followBlogUser(self, follow:UserBean):
        """
        爬取关注用户信息
        :return:
        """
        # 储存在redis数据库
        if not self.redisPool.redis.hexists(name=self.redis_user, key=int(follow.blogId)):
            self.redisPool.redis.hset(name=self.redis_user, key=int(follow.blogId), value=self.entityToJson(follow))
        # 存储在mysql数据库
        # sql = sql = "INSERT INTO userInfo (blogId,blogName) VALUES (%s,%s)  ON DUPLICATE KEY UPDATE blogName=%s"

        result = self.mysqlPool.getOne(sql="SELECT blogId,postAddTime FROM userInfo WHERE blogId=%s",param=[follow.blogId])
        if not result:
            self.mysqlPool.insert(
                sql="INSERT INTO userInfo (blogId,blogName,homePageUrl,postAddTime,postModTime) VALUES (%s,%s,%s,%s,%s)",
                param=[
                    follow.blogId,
                    follow.blogInfo.blogName,
                    follow.blogInfo.homePageUrl,
                    int(follow.blogInfo.postAddTime),
                    int(follow.blogInfo.postModTime)
                ]
            )
            self.mysqlPool.end()

        else:

            if int(str(result.get("postAddTime"),encoding="utf-8"))>=int(follow.blogInfo.postAddTime):
                # 不需要爬取

                return False
            self.mysqlPool.update(
                sql="UPDATE userInfo SET blogName=%s ,  homePageUrl=%s , postAddTime=%s,postModTime=%s WHERE blogId=%s",
                param=[
                    follow.blogInfo.blogName,
                    follow.blogInfo.homePageUrl,
                    int(follow.blogInfo.postAddTime),
                    int(follow.blogInfo.postModTime),
                    follow.blogId
                ]
            )
            self.mysqlPool.end()
        return True

    def get_userArchive(self, follow: UserBean,archives:List[Archive]):
        """
        爬取归档信息
        :param follow:
        :param kwargs:
        :return:
        """
        for archive in archives:
            key = "{}&{}".format(follow.blogId,archive.id)
            if not self.redisPool.redis.hexists(name=self.redis_view,key=key):
                self.redisPool.redis.hset(name=self.redis_view,key=key,value=self.entityToJson(archive))

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
