#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 20:26
@Project:LofterSpider
@File:Archive.py
@Desc:
'''
        
class Archive(object):

	def __init__(self):
		self.__blogId = None
		self.__cctype = None
		self.__collectionId = None
		self.__dayOfMonth = None
		self.__id = None
		self.__month = None
		self.__noteCount = None
		self.__reblog = None
		self.__tagCount = None
		self.__time = None
		self.__type = None
		self.__valid = None
		self.__values = None
		self.__year = None
	@property
	def blogId(self):
		return self.__blogId

	@blogId.setter
	def blogId(self, blogId):
		self.__blogId = blogId

	@property
	def cctype(self):
		return self.__cctype

	@cctype.setter
	def cctype(self, cctype):
		self.__cctype = cctype

	@property
	def collectionId(self):
		return self.__collectionId

	@collectionId.setter
	def collectionId(self, collectionId):
		self.__collectionId = collectionId

	@property
	def dayOfMonth(self):
		return self.__dayOfMonth

	@dayOfMonth.setter
	def dayOfMonth(self, dayOfMonth):
		self.__dayOfMonth = dayOfMonth

	@property
	def id(self):
		return self.__id

	@id.setter
	def id(self, id):
		self.__id = id

	@property
	def month(self):
		return self.__month

	@month.setter
	def month(self, month):
		self.__month = month

	@property
	def noteCount(self):
		return self.__noteCount

	@noteCount.setter
	def noteCount(self, noteCount):
		self.__noteCount = noteCount

	@property
	def reblog(self):
		return self.__reblog

	@reblog.setter
	def reblog(self, reblog):
		self.__reblog = reblog

	@property
	def tagCount(self):
		return self.__tagCount

	@tagCount.setter
	def tagCount(self, tagCount):
		self.__tagCount = tagCount

	@property
	def time(self):
		return self.__time

	@time.setter
	def time(self, time):
		self.__time = time

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):
		self.__type = type

	@property
	def valid(self):
		return self.__valid

	@valid.setter
	def valid(self, valid):
		self.__valid = valid

	@property
	def values(self):
		return self.__values

	@values.setter
	def values(self, values):
		self.__values = values

	@property
	def year(self):
		return self.__year

	@year.setter
	def year(self, year):
		self.__year = year

