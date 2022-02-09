#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 20:26
@Project:LofterSpider
@File:Archivevalues.py
@Desc:
'''
        
class ArchiveValues(object):

	def __init__(self):
		self.__imgurl = None
		self.__permalink = None
		self.__noticeLinkTitle = None
		self.__images = None

	@property
	def imgurl(self):
		return self.__imgurl

	@imgurl.setter
	def imgurl(self, imgurl):
		self.__imgurl = imgurl

	@property
	def images(self):
		return self.__images

	@images.setter
	def images(self, images):
		self.__images = images

	@property
	def permalink(self):
		return self.__permalink

	@permalink.setter
	def permalink(self, permalink):
		self.__permalink = permalink

	@property
	def noticeLinkTitle(self):
		return self.__noticeLinkTitle

	@noticeLinkTitle.setter
	def noticeLinkTitle(self, noticeLinkTitle):
		self.__noticeLinkTitle = noticeLinkTitle

