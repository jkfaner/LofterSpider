#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 12:04
@Project:LofterSpider
@File:spiderIter.py
@Desc:
"""
import re

from lxml import etree

from Extractor.jsonExtractorDWR import ExtractorDWRAPI
from Extractor.loftExtractorAPI import LoftExtractorAPI
from Session.spiderRequest import SessionRequest
from util.decorator import desc_time
from util.logger import logger
from util.queue import Queue


class SpiderIter(SessionRequest, ExtractorDWRAPI, LoftExtractorAPI):

    def getUserFollowingList(self, nums: int = 1000, order_by_follow=True) -> Queue:
        """
        获取关注列表数据
        :return:
        """
        response = super(SpiderIter, self).getUserFollowingList(nums, order_by_follow)
        dwr_dict = self.getDict(response.text)
        follow_queue = self.extractorFollow(dwr=dwr_dict)
        return follow_queue

    def getUserArchiveList(self, blogName: str, blogId: int, timestamp: int, nums=1000) -> Queue:
        """
        获取归档数据
        :param blogName:
        :param blogId:
        :param timestamp:
        :param nums:
        :return:
        """
        response = super(SpiderIter, self).getUserArchiveList(blogName, blogId, timestamp, nums)
        dwr_dict = self.getDict(response.text)
        archive_queue = self.extractorArchive(dwr=dwr_dict)
        return archive_queue

    def getUserArchiveIter(self, blogName: str, blogId: int, timestamp: int, total=1000) -> iter:
        """
        获取全部归档数据
        :param blogName:
        :param blogId:
        :param timestamp:
        :param total:单次量
        :return:迭代对象
        """
        archive_queue = self.getUserArchiveList(blogName, blogId, timestamp, total)
        archive_data = archive_queue.get_all()
        if archive_data:
            logger.info(f"归档信息获取中：{blogName} -> {blogId} -> {timestamp}")
            yield archive_data
            timestamp = int(min([_.time for _ in archive_data]))
            yield from self.getUserArchiveIter(blogName, blogId, timestamp, total)

    @staticmethod
    def __extractorByXpath(response):
        """
        通过xpath解析
        :param response:
        :return:
        """
        try:
            html = etree.HTML(response.content.decode("utf-8"))
            imageElements = html.xpath(
                "//a[@class='imgclasstag' or @class='img imgclasstag' or @class='img-lnk imgclasstag']")
        except AttributeError:
            return []
        return imageElements

    @staticmethod
    def __extractorByRe(response):
        """
        通过正则解析
        :param response:
        :return:
        """
        images = list()
        for img in re.findall(r'bigimgsrc="(.*)">', (response.content.decode("utf-8"))):
            images.append(img.split("?")[0])
        return images

    @desc_time(0)
    def getHtmlPage(self, blogName: str, permalink: str) -> Queue:
        """
        解析网页图片
        :param blogName:
        :param permalink:
        :return:
        """

        response = super(SpiderIter, self).getHtmlPage(blogName, permalink)
        imageElements = self.__extractorByXpath(response)
        queueXpath = Queue()
        for image in imageElements:
            try:
                url = re.search(r"(.*net/img/.*\.[jnpegif]{3,4})", image.attrib['bigimgsrc']).group(1)
                queueXpath.enqueue(url)
            except AttributeError:
                # 图片损坏
                pass

        queueRe = Queue()
        for image in self.__extractorByRe(response):
            queueRe.enqueue(image)
        imagesXpath = len(queueXpath.get_all())
        imagesRe = len(queueRe.get_all())
        logger.info("XPath解析：图片{}张 正则解析：图片{}张".format(imagesXpath,imagesRe))
        return queueRe if imagesXpath <= imagesRe else imagesXpath
