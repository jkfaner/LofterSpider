# coding=utf-8
# /usr/bin/ python3

'''
Author:极客说_范儿
Email:geektalk@qq.com
Wechat & QQ:601872868

date:2020/3/2 10:55 下午
dese:getUserFollowingList（获取用户关注列表）获取自己关注的UP主
'''
import json
import os
import re
import sys
import requests


init_path = os.path.split(os.path.realpath(__file__))[0] + os.sep

header = {"Referer": "https://www.lofter.com/",
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) Apple"
                        "WebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
payload = {"callCount": 1,
           "scriptSessionId": "${scriptSessionId}187",
           "httpSessionId": '',
           "c0-scriptName": "UserBean",
           "c0-methodName": "getUserFollowingList",
           "c0-id": 0,
           "c0-param0": "number:10000",
           "c0-param1": "number:0",
           "c0-param2": "boolean:false",
           "batchId": 1,
           }

with open(init_path + "config_user.json", 'r')as f:
    info = json.loads(f.read())
    header["Cookie"] = info["Cookie"]
    RenameFolder = info["RenameFolder"]

dwr_url = "https://www.lofter.com/dwr/call/plaincall/UserBean.getUserFollowingList.dwr"
response = requests.post(url=dwr_url, data=payload, headers=header).text

if "dwr.engine._remoteHandleCallback('1','0',null);" in response:
    sys.exit(u"Cookie不存在或者过期...")
else:
    domains = re.findall(r'homePageUrl="https://(.*).lofter.com"', response)
    blogids = re.findall(r"blogId=(\d*);", response)
    user_names = re.findall('s[0-9]{1,4}.blogNickName="(.*)";s[0-9]{1,4}\.blogStat=', response)

# 获取三级域名
UserDomain = []
for domain in domains:
    UserDomain.append(domain)

# 博客id去重并获取博客id
BlogIds = []
for blogid in blogids:  # 不可使用set()去重,不然后面字典键值对不匹配
    if blogid not in BlogIds:
        BlogIds.append(blogid)

# 获取博客名
blogNickName = []
for user_name in user_names:
    user_name = user_name.encode('utf8').decode('unicode_escape')
    blogNickName.append(user_name)

USER_LIST = []
for userno, user in enumerate(UserDomain, 1):
    user_dict = {
        "userNo": userno,   # 用户编号
        "blogNickName": blogNickName[userno-1],  # 博客昵称
        "blogId": BlogIds[userno-1],    # 用户博客id
        "userDomain": UserDomain[userno-1],  # 用户三级域名
        "RenameFolder": RenameFolder    # 更改文件夹参数
    }
    USER_LIST.append(user_dict)
    
USERS = USER_LIST
