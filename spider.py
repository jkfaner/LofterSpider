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
import json
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

    def get_userArchive(self, follow: UserBean) -> List[Archive]:
        """
        爬取归档信息
        :param follow:用户对象
        :return:
        """
        # 获取归档
        logger.info("正在获取{}的所有归档信息...".format(follow.blogInfo.blogNickName))
        archives_list = list()
        for ss in self.spiderObj.getUserArchiveIter(blogName=follow.blogInfo.blogName, blogId=int(follow.blogId),timestamp=self.time()):
            archives_list.extend(ss)
        archives_len = len(archives_list)
        logger.info("已获取归档信息{}条...".format(archives_len))
        return archives_list

    def get_permalinkPage(self, follow: UserBean=None, archive: Archive=None, index: int = None, total: int = None, **kwargs):
        """
        解析页面
        :param follow:用户对象
        :param archive:归档对象
        :param index:索引
        :param total:合计
        :param kwargs:
        :return:
        """
        if super(Spider, self).get_permalinkPage(follow, archive, index, total):
            blogId = int(follow.blogId)
            blogName = follow.blogInfo.blogName
            permalink = archive.values.permalink

            images = self.spiderObj.getHtmlPage(blogName=blogName, permalink=permalink)
            images_list = images.get_all()
            archive.values.images = images_list
            key = "{}&{}".format(blogId, permalink)
            logger.info(f"[{index}/{total}]网页解析信息：{blogId} -> {blogName} -> {permalink} -> {key} -> 图片:{len(images_list)}")
            archive_json = json.dumps(archive, default=lambda archive: {
                k.split("__")[-1]: v
                for k, v in archive.__dict__.items()
            })
            super(Spider, self).get_permalinkPage(archive_json=archive_json)

    def spider_images(self):
        for follow in self.get_followBlogUser():
            archives_list = self.get_userArchive(follow)
            for index, archive in enumerate(archives_list, 1):
                print(type(archive))
                self.get_permalinkPage(follow, archive, index, len(archives_list))


if __name__ == '__main__':
    s = Spider()
    s.spider_images()
