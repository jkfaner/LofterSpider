#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 11:46
@Project:LofterSpider
@File:spider.py
@Desc:
"""
from typing import List

from Extractor.entity.archive import Archive
from Extractor.entity.userBean import UserBean
from Session.spiderMiddleware import SpiderMiddleware
from util.logger import logger


class Spider(SpiderMiddleware):

    def get_followBlogUser(self, follow=None):
        """
        爬取关注用户信息
        :param follow:
        :return:
        """
        # 获取关注数据
        logger.info("正在获取关注信息...")
        follow_queue = self.spiderObj.getUserFollowingList()
        for follow in follow_queue.get_all():
            super(Spider, self).get_followBlogUser(follow)
            yield follow

    def get_userArchive(self, follow: UserBean, **kwargs) -> List[Archive]:
        """
        爬取归档信息
        :param follow:用户对象
        :return:
        """
        # 获取归档
        logger.info("正在获取{}的所有归档信息...".format(follow.blogInfo.blogNickName))
        archives_list = list()
        for ss in self.spiderObj.getUserArchiveIter(
                blogName=follow.blogInfo.blogName,
                blogId=int(follow.blogId),
                timestamp=self.time(),
                total=1000):
            archives_list.extend(ss)
        logger.info("已获取归档信息{}条...".format(len(archives_list)))
        return archives_list

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
        archive_info = super(Spider, self).get_permalinkPage(follow, archive, index, total)
        if not archive_info:
            images = self.spiderObj.getHtmlPage(
                blogName=follow.blogInfo.blogName,
                permalink=archive.values.permalink
            )
            archive.values.images = images.get_all()
            key = "{}&{}".format(int(follow.blogId), archive.values.permalink)
            logger.info(
                f"[{index}/{total}]网页解析信息：{int(follow.blogId)} "
                f"-> {follow.blogInfo.blogName} "
                f"-> {archive.values.permalink} "
                f"-> {key} -> 图片:{len(archive.values.images)}"
            )
            archive_info = super(Spider, self).get_permalinkPage(follow, archive)
        return archive_info

    def run(self):
        """
        爬取关注用的所有图片
        :return:
        """
        for follow in self.get_followBlogUser():
            archives_list = self.get_userArchive(follow)
            len_archives = len(archives_list)
            for index, archive in enumerate(archives_list, 1):
                archive_info = self.get_permalinkPage(follow, archive, index, len_archives)