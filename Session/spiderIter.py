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

    def getUserArchiveIter(self, blogName: str, blogId: int, timestamp: int, nums=1000) -> iter:
        """
        获取全部归档数据
        :param blogName:
        :param blogId:
        :param timestamp:
        :param nums:单次量
        :return:迭代对象
        """
        archive_queue = self.getUserArchiveList(blogName, blogId, timestamp, nums)
        archive_data = archive_queue.get_all()
        if archive_data:
            yield archive_data
            timestamp = int(min([_.time for _ in archive_data]))
            yield from self.getUserArchiveIter(blogName, blogId, timestamp, nums)

    @desc_time(0)
    def getHtmlPage(self, blogName: str, permalink: str) -> Queue:
        """
        解析网页图片
        :param blogName:
        :param permalink:
        :return:
        """
        response = super(SpiderIter, self).getHtmlPage(blogName, permalink)
        html_code = response.content.decode("utf-8")
        html = etree.HTML(html_code)
        imageElements = html.xpath("//a[@class='imgclasstag' or @class='img imgclasstag']")
        queue = Queue()
        if imageElements:
            for image in imageElements:
                try:
                    url = re.search(r"(.*net/img/.*\.[jnpegif]{3,4})", image.attrib['bigimgsrc']).group(1)
                    queue.enqueue(url)
                except AttributeError:
                    # 图片损坏
                    pass
        else:
            for img in re.findall(r'bigimgsrc="(.*)">', html_code):
                queue.enqueue(img.split("?")[0])
        return queue
