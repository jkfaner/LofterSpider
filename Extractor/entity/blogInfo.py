#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/2/2 20:26
@Project:LofterSpider
@File:blogInfo.py
@Desc:
'''


class BlogInfo(object):

    def __init__(self):
        self.__acceptGift = None
        self.__acceptReward = None
        self.__auths = None
        self.__avaUpdateTime = None
        self.__avatarBoxId = None
        self.__avatarBoxImage = None
        self.__avatarBoxName = None
        self.__bigAvaImg = None
        self.__birthday = None
        self.__blogCreateTime = None
        self.__blogId = None
        self.__blogLiverInfo = None
        self.__blogName = None
        self.__blogNickName = None
        self.__blogStat = None
        self.__commentRank = None
        self.__gendar = None
        self.__homePageUrl = None
        self.__imageDigitStamp = None
        self.__imageProtected = None
        self.__imageStamp = None
        self.__ip = None
        self.__isOriginalAuthor = None
        self.__keyTag = None
        self.__novisible = None
        self.__postAddTime = None
        self.__postModTime = None
        self.__remarkName = None
        self.__rssFileId = None
        self.__rssGenTime = None
        self.__selfIntro = None
        self.__signAuth = None
        self.__smallAvaImg = None
        self.__star = None
        self.__unauths = None
        self.__verifyBlog = None

    @property
    def acceptGift(self):
        return self.__acceptGift

    @acceptGift.setter
    def acceptGift(self, acceptGift):
        self.__acceptGift = acceptGift

    @property
    def acceptReward(self):
        return self.__acceptReward

    @acceptReward.setter
    def acceptReward(self, acceptReward):
        self.__acceptReward = acceptReward

    @property
    def auths(self):
        return self.__auths

    @auths.setter
    def auths(self, auths):
        self.__auths = auths

    @property
    def avaUpdateTime(self):
        return self.__avaUpdateTime

    @avaUpdateTime.setter
    def avaUpdateTime(self, avaUpdateTime):
        self.__avaUpdateTime = avaUpdateTime

    @property
    def avatarBoxId(self):
        return self.__avatarBoxId

    @avatarBoxId.setter
    def avatarBoxId(self, avatarBoxId):
        self.__avatarBoxId = avatarBoxId

    @property
    def avatarBoxImage(self):
        return self.__avatarBoxImage

    @avatarBoxImage.setter
    def avatarBoxImage(self, avatarBoxImage):
        self.__avatarBoxImage = avatarBoxImage

    @property
    def avatarBoxName(self):
        return self.__avatarBoxName

    @avatarBoxName.setter
    def avatarBoxName(self, avatarBoxName):
        self.__avatarBoxName = avatarBoxName

    @property
    def bigAvaImg(self):
        return self.__bigAvaImg

    @bigAvaImg.setter
    def bigAvaImg(self, bigAvaImg):
        self.__bigAvaImg = bigAvaImg

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    @property
    def blogCreateTime(self):
        return self.__blogCreateTime

    @blogCreateTime.setter
    def blogCreateTime(self, blogCreateTime):
        self.__blogCreateTime = blogCreateTime

    @property
    def blogId(self):
        return self.__blogId

    @blogId.setter
    def blogId(self, blogId):
        self.__blogId = blogId

    @property
    def blogLiverInfo(self):
        return self.__blogLiverInfo

    @blogLiverInfo.setter
    def blogLiverInfo(self, blogLiverInfo):
        self.__blogLiverInfo = blogLiverInfo

    @property
    def blogName(self):
        return self.__blogName

    @blogName.setter
    def blogName(self, blogName):
        self.__blogName = blogName

    @property
    def blogNickName(self):
        return self.__blogNickName

    @blogNickName.setter
    def blogNickName(self, blogNickName):
        self.__blogNickName = blogNickName

    @property
    def blogStat(self):
        return self.__blogStat

    @blogStat.setter
    def blogStat(self, blogStat):
        self.__blogStat = blogStat

    @property
    def commentRank(self):
        return self.__commentRank

    @commentRank.setter
    def commentRank(self, commentRank):
        self.__commentRank = commentRank

    @property
    def gendar(self):
        return self.__gendar

    @gendar.setter
    def gendar(self, gendar):
        self.__gendar = gendar

    @property
    def homePageUrl(self):
        return self.__homePageUrl

    @homePageUrl.setter
    def homePageUrl(self, homePageUrl):
        self.__homePageUrl = homePageUrl

    @property
    def imageDigitStamp(self):
        return self.__imageDigitStamp

    @imageDigitStamp.setter
    def imageDigitStamp(self, imageDigitStamp):
        self.__imageDigitStamp = imageDigitStamp

    @property
    def imageProtected(self):
        return self.__imageProtected

    @imageProtected.setter
    def imageProtected(self, imageProtected):
        self.__imageProtected = imageProtected

    @property
    def imageStamp(self):
        return self.__imageStamp

    @imageStamp.setter
    def imageStamp(self, imageStamp):
        self.__imageStamp = imageStamp

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def isOriginalAuthor(self):
        return self.__isOriginalAuthor

    @isOriginalAuthor.setter
    def isOriginalAuthor(self, isOriginalAuthor):
        self.__isOriginalAuthor = isOriginalAuthor

    @property
    def keyTag(self):
        return self.__keyTag

    @keyTag.setter
    def keyTag(self, keyTag):
        self.__keyTag = keyTag

    @property
    def novisible(self):
        return self.__novisible

    @novisible.setter
    def novisible(self, novisible):
        self.__novisible = novisible

    @property
    def postAddTime(self):
        return self.__postAddTime

    @postAddTime.setter
    def postAddTime(self, postAddTime):
        self.__postAddTime = postAddTime

    @property
    def postModTime(self):
        return self.__postModTime

    @postModTime.setter
    def postModTime(self, postModTime):
        self.__postModTime = postModTime

    @property
    def remarkName(self):
        return self.__remarkName

    @remarkName.setter
    def remarkName(self, remarkName):
        self.__remarkName = remarkName

    @property
    def rssFileId(self):
        return self.__rssFileId

    @rssFileId.setter
    def rssFileId(self, rssFileId):
        self.__rssFileId = rssFileId

    @property
    def rssGenTime(self):
        return self.__rssGenTime

    @rssGenTime.setter
    def rssGenTime(self, rssGenTime):
        self.__rssGenTime = rssGenTime

    @property
    def selfIntro(self):
        return self.__selfIntro

    @selfIntro.setter
    def selfIntro(self, selfIntro):
        self.__selfIntro = selfIntro

    @property
    def signAuth(self):
        return self.__signAuth

    @signAuth.setter
    def signAuth(self, signAuth):
        self.__signAuth = signAuth

    @property
    def smallAvaImg(self):
        return self.__smallAvaImg

    @smallAvaImg.setter
    def smallAvaImg(self, smallAvaImg):
        self.__smallAvaImg = smallAvaImg

    @property
    def star(self):
        return self.__star

    @star.setter
    def star(self, star):
        self.__star = star

    @property
    def unauths(self):
        return self.__unauths

    @unauths.setter
    def unauths(self, unauths):
        self.__unauths = unauths

    @property
    def verifyBlog(self):
        return self.__verifyBlog

    @verifyBlog.setter
    def verifyBlog(self, verifyBlog):
        self.__verifyBlog = verifyBlog
