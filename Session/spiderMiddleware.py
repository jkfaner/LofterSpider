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
from Session.sessionMiddleware import SessionMiddleware
from loftInit import LoftInit


class SpiderMiddleware(LoftInit, SessionMiddleware):
    redis_user = "userBean"
    redis_archive = "archive"

    def get_followBlogUser(self, follow):
        """
        爬取关注用户信息
        :return:
        """
        blogId = int(follow.blogId)
        if not self.redisPool.redis.hexists(name=self.redis_user, key=blogId):
            follow_json = json.dumps(follow, default=lambda follow: {
                k.split("__")[-1]: v for k, v in follow.__dict__.items()
            })
            self.redisPool.redis.hset(name=self.redis_user, key=blogId, value=follow_json)

    def get_userArchive(self, follow: UserBean) -> List[UserBean]:
        """
        爬取归档信息
        :param follow:
        :return:
        """
        pass

    def get_permalinkPage(self, follow: UserBean=None, archive:Archive=None, index:int=None, total:int=None, **kwargs):
        key = "{}&{}".format(int(follow.blogId), archive.values.permalink)
        if kwargs.get("archive_json"):
            self.redisPool.redis.hset(name=self.redis_archive, key=key, value=kwargs.get("archive_json"))
            return False
        if not self.redisPool.redis.hexists(name=self.redis_archive, key=key):
            return True
        return False
