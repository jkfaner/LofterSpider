# 网易Lofter 图片爬虫
* [功能](#功能)
* [实例](#实例)
  * [版本V1.0](#版本V1.0)
  * [版本V1.1](#版本V1.1)
* [版本更新信息](#版本更新信息)
  * [版本V1.0](#版本V1.0)
  * [版本V1.1](#版本V1.1)
## 功能

分段爬取网易Lofter（乐乎）博主的数据，并将数据写本地。写入的信息几乎包括博主的所有数据， 主要有源数据和图片数据，前者包含博主归档页html（[版本V1.0特有](https://github.com/jkfaner/LofterSpider/tree/master/LofterSpiderV1.0)）、DWR数据、详情页数据、图片地址数据，后者包括图片数据。

**具体的写入文件类型如下：**

- 写入归档页.html（[版本V1.0特有](https://github.com/jkfaner/LofterSpider/tree/master/LofterSpiderV1.0)）

- 写入DWR.txt（默认）
- 写入htmlURL.json（默认）
- 写入imageURL.json（默认）
- 下载博主的所有原图片（默认）

程序可实现爬取结果自动更新，即：现在爬取博主的信息后，一段时间后，目标用户可能更新了，再次运行将下载用户更新的数据。

## 实例

### 版本V1.0

以爬取[LOFTER官方博客](http://i.lofter.com/)的数据，我们需要将博主的**三级域名**放入配置文件（**config.json**）中，例如：

```json
{
  "user_id_list": ["i","brandfans"]
}
```

爬取后的数据如下：

![](https://github.com/jkfaner/img-folder/blob/master/LofterSpider/tree.png)

![](https://github.com/jkfaner/img-folder/blob/master/LofterSpider/html.png)

![](https://github.com/jkfaner/img-folder/blob/master/LofterSpider/image.png)

### 版本V1.1

在1.0版本中，当我们要爬取大量用户的图片时，手动添加博主的三级域名显得十分繁琐。在V1.1版本中，我们可以通过自己的账号来爬取自己关注的博主。所以我们想爬谁，就关注谁。在此之前我们需要获取自己账号的Cookie值来进行程序与服务器之间的会话。

我们需要将Cookie值放入配置文件（**config_user.json**）中：

```json
{
  "Cookie": ""
}
```

爬取后的数据如下：

![](https://github.com/jkfaner/img-folder/blob/master/LofterSpider/treeV1.1.png)

![](https://github.com/jkfaner/img-folder/blob/master/LofterSpider/htmlV1.1.png)

![](https://github.com/jkfaner/img-folder/blob/master/LofterSpider/imageV1.1.png)

## 版本更新信息

## V1.0

**项目文件包含：**

1. config.json
2. LofterSpier.py

***功能：***

实现网易Lofter个人原图采集。



## V1.1

**项目文件包含：**

1. config_user.json
2. getUserFollowingList.py
3. LofterSpider.py
4. logger.py

**功能：**

- [x] 新增：自动获取博主信息，无需配置，只需关注
- [x] 新增：多进程并行下载，让图片下载更快
- [x] 新增：Log日志，让运行情况更明确
- [x] 优化：优化部分代码，提高爬虫效率
- [x] 优化：优化文件夹命名