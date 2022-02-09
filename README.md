# ![网易Lofter](https://lofter.lf127.net/1610534500868/logo.png) 
# 网易Lofter爬虫

* [功能](#功能)
* [使用方法](#使用方法)
* [爬取结果](#爬取结果)
  
## 功能
爬取网易Lofter博主的个人信息、个人发布的所有图片。

## 使用方法
- 1.获取源代码与依赖配置
```
git clone https://github.com/jkfaner/LofterSpider.git
pip install -r requests.txt
```
- 2.配置config.ini参数
```
[login]
username = 用户名
password = 密码

[mysql]
host = localhost
port = 3306
user = mysql账户
pwd = mysql密码
db_name = mysql数据库名

[redis]
host = localhost
port = 6379
password =
db = 0
```
- 3.开启mysql server 和 redis server
- 4.创建mysql数据表
```mysql
CREATE TABLE `login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `userid` int DEFAULT NULL,
  `deviceid` varchar(255) DEFAULT NULL,
  `token` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`,`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
- 5.运行main.py
## 爬取结果
![爬取结果](img/WX20220209-203936@2x.png)