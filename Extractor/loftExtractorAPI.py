#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/8 11:55
@Project:LofterSpider
@File:loftExtractorAPI.py
@Desc:
"""
from Extractor.entity.archive import Archive
from Extractor.entity.archiveValues import ArchiveValues
from Extractor.entity.blogInfo import BlogInfo
from Extractor.entity.userBean import UserBean
from Extractor.jsonExtractorAPI import ExtractorApi
from util.queue import Queue


class LoftExtractorAPI(ExtractorApi):

    def extractorFollow(self, dwr: dict) -> Queue:
        """
        解析乐乎关注的数据
        :param dwr:
        :return:
        """
        blog = self.find_first_level_data(dwr, "blogId")
        blogInfo = self.find_all_data(blog, "blogInfo")
        for n, _ in enumerate(blog):
            if "blogInfo" in _:
                del _["blogInfo"]

        userBeanObj_list = list()
        for _blog in blog:
            userBeanObj = UserBean()
            for k, v in userBeanObj.__dict__.items():
                targ = k.split("__")[-1]
                setattr(userBeanObj, targ, self.find_first_data(_blog, targ))
            userBeanObj_list.append(userBeanObj)

        blogInfoObj_list = list()
        for _blogInfo in blogInfo:
            blogInfoObj = BlogInfo()
            for k, v in blogInfoObj.__dict__.items():
                targ = k.split("__")[-1]
                setattr(blogInfoObj, targ, self.find_first_data(_blogInfo, targ))
            blogInfoObj_list.append(blogInfoObj)

        queue = Queue()
        for u in userBeanObj_list:
            for b in blogInfoObj_list:
                if u.blogId == b.blogId:
                    u.blogInfo = b
                    queue.enqueue(u)
        return queue

    def extractorArchive(self, dwr: dict) -> Queue:
        """
        提取归档数据
        :param dwr:
        :return:
        """
        queue = Queue()
        archives = self.find_first_level_data(dwr, "blogId")
        for _archive in archives:
            archiveObj = Archive()
            for k, v in _archive.items():
                if k == "values":
                    archiveValuesObj = ArchiveValues()
                    for _k, _v in v.items():
                        setattr(archiveValuesObj, _k, _v)
                    archiveObj.values = archiveValuesObj
                else:
                    setattr(archiveObj, k, v)
            queue.enqueue(archiveObj)
        return queue
