# coding=utf-8
# /usr/bin/ python3

'''
Author:极客说_范儿
Email:geektalk@qq.com
Wechat & QQ:601872868

date:2020/2/8 1:18 上午
dese:实现网易Lofter图片采集
'''

import re
import time
import requests
import os
import json
from lxml import etree
from concurrent import futures
from logger import logger
from getUserFollowingList import USERS as userInfos



init_path = os.path.split(os.path.realpath(__file__))[0] + os.sep

class SpiderMethod(object):

    def __init__(self):
        self.g_parent_path = init_path + "LoftResources/"
        self.parent_path = ''
        self.dwr_path = ''
        self.url_path = ''
        self.html_path = ''
        self.image_path = ''
        self.image_url_path = ''
        self.image_filename = ''
        self.url_list = ''
        self.filename_list = ''
        self.image_dict = ''
        self.url_dict = ''
        self.url = ''
        self.payload = ''
        self.headers = ''

    @staticmethod
    def create_directory(path):
        """检查和创建目录"""
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def check_file(path):
        """
        需要一个正确的路径,检查检查文件是否存在
        :return:True or False
        """
        return os.path.exists(path)

    @staticmethod
    def get_html(url):
        """获取用户html"""
        # 需要添加header，模拟浏览器访问
        html = requests.get(url=url).content
        return html

    @staticmethod
    def writ_file(path, data):
        """写入信息到本地"""
        if isinstance(data, bytes):
            with open(path, "wb") as f:
                f.write(data)
        elif isinstance(data, str):
            with open(path, 'a', encoding="utf-8") as f:
                f.write(data)
        elif isinstance(data, dict):
            with open(path, 'w', encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False))

    @staticmethod
    def read_file(path):
        """读取目录下的文件"""
        with open(path, 'r', encoding="utf-8") as f:
            data = f.read()
            return data


class Loft(SpiderMethod):
    """乐乎个人爬虫"""

    def dwr_headers(self, userInfo):
        """初始化headers"""
        url = 'http://{userDomain}.lofter.com/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr'.format(**userInfo)
        self.payload = {
            "callCount": "1",
            "scriptSessionId": "${scriptSessionId}187",
            "httpSessionId": "",
            "c0-scriptName": "ArchiveBean",
            "c0-methodName": "getArchivePostByTime",
            "c0-id": "0",
            "c0-param0": "boolean:false",
            "c0-param1": "number:{blogId}".format(**userInfo),
            "c0-param3": "number:50",
            "c0-param4": "boolean:false",
            "batchId": "1"}
        self.headers = {
            "Content-Type": "text/plain",
            'Referer': 'https://{userDomain}.lofter.com/view'.format(**userInfo),
            "Host": "{userDomain}.lofter.com".format(**userInfo),
            "Origin": "https://{userDomain}.lofter.com".format(**userInfo),
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, "
            "like Gecko) Chrome/79.0.3945.79 Safari/537.36 ",
        }
        return url

    def get_dwr(self, url):
        """获取dwr"""
        time.sleep(0.1)
        dwr = requests.post(url, data=self.payload, headers=self.headers).text
        return dwr

    def init_path(self, userInfo):
        """初始化文件（夹）路径"""
        self.parent_path = self.g_parent_path + "[博主]_{blogNickName}/".format(**userInfo)
        self.dwr_path = self.parent_path + "DWR.txt"
        self.url_path = self.parent_path + "htmlURL.json"
        self.html_path = self.parent_path + "html/"
        self.image_path = self.parent_path + "img/"
        self.image_url_path = self.parent_path + "imageURL.json"

    def write_permalink_dict(self, permalinks, userInfo):
        """匹配详情页面url"""
        url_list = []
        for permalink in permalinks:
            url = "https://{userDomain}.lofter.com/post/{permalink}".format(**userInfo, permalink=permalink)
            url_list.append(url)
        permalink_dict = dict(zip(permalinks, url_list))
        self.writ_file(self.url_path, permalink_dict)

    def get_new_dwr(self, url):
        """获取最新dwr"""
        self.payload["c0-param2"] = "number:{}".format(str(time.time() * 1000)[:13])
        dwr = self.get_dwr(url)
        with open(self.dwr_path, 'w', encoding="utf-8") as f:
            f.write(dwr)

    def get_other_dwr(self, url):
        """获取其他dwr"""
        while True:
            dwr = self.read_file(self.dwr_path)
            if "dwr.engine._remoteHandleCallback('1','0',[]);" in dwr:
                # print(" dwr采集结束...")
                break
            try:
                time_list = re.findall("time=([0-9]*);", dwr)
            except AttributeError:
                logger.info("No dwr data was collected or the user did not post a picture.")
            else:
                self.payload["c0-param2"] = "number:{}".format(time_list[-1])
                dwr = self.get_dwr(url)
                self.writ_file(self.dwr_path, dwr)

    def getData_module(self):
        """采集DWR-详情页URL"""
        for userInfo in userInfos:
            self.init_path(userInfo)
            self.create_directory(self.g_parent_path)
            self.create_directory(self.parent_path)
            logger.info('Task No.{userNo} [{blogNickName}] Get dwr...'.format(**userInfo))
            time0 = time.time()
            url = self.dwr_headers(userInfo)
            self.get_new_dwr(url)
            self.get_other_dwr(url)
            logger.info("Task No.{userNo} [{blogNickName}] Get urls...".format(**userInfo))
            dwr = self.read_file(self.dwr_path)
            permalinks = re.findall("""permalink="([0-9a-z_]*)";""", dwr)
            if not self.check_file(self.url_path):
                self.write_permalink_dict(permalinks, userInfo)
            if not len(json.load(open(self.url_path))) == len(permalinks):
                logger.info(" Data incomplete ... collected again ...")
                self.write_permalink_dict(permalinks, userInfo)
            message = "Task No.{userNo} [{blogNickName}] Get [DWR.txt htmlURL.json] Success! run {time:.2f} seconds"
            logger.info(message.format(**userInfo, time=time.time()-time0))

    def get_html_code(self, url, userInfo):
        if not self.check_file(self.html_path + "{filename}.html".format(**url)):
            try:
                time.sleep(0.5)
                html = self.get_html(url["link"]).decode("utf-8")
            except Exception as e:
                print("%s\n" % e)
            else:
                self.writ_file(self.html_path + "{filename}.html".format(**url), html)
                message = "Task No.{userNo} [{blogNickName}] Download {filename}.html"
                logger.info(message.format(**userInfo, **url))

    def getPagesHtml_module(self):
        """采集详情页html"""
        for userInfo in userInfos:
            logger.info('Task No.{userNo} [{blogNickName}] Get all pages...'.format(**userInfo))
            self.init_path(userInfo)
            url_dict = json.load(open(self.url_path))
            self.create_directory(self.html_path)
            keys = list(url_dict.keys())
            values = list(url_dict.values())
            urls = []
            for i in range(len(values)):
                image = {
                    'filename': keys[i],
                    'link': values[i],
                }
                urls.append(image)
            time0 = time.time()
            # 单线程（主线程）
            for url in urls:
                self.get_html_code(url, userInfo)

            # # 多线程（会封ip，慢点操作）
            # workers = min(64, len(urls))
            # with futures.ThreadPoolExecutor(workers) as executor:
            #     to_do = []
            #     for url in urls:
            #         future = executor.submit(self.get_html_code, url)
            #         to_do.append(future)
            #     results = []
            #     for future in futures.as_completed(to_do):
            #         res = future.result()
            #         results.append(res)
            #         logger.debug('{} result: {!r}'.format(future, res))
            message = 'Task No.{userNo} [{blogNickName}] Get all pages Success! run {time:.2f}'
            logger.info(message.format(**userInfo, time=time0-time.time()))

    def image_url_match(self, images):
        """图片地址匹配"""
        for image in images:
            try:
                image_url = re.search(
                    r"(.*net/img/.*\.[jnpegif]{3,4})?",
                    image.attrib['bigimgsrc']).group(1)
                image_filename = re.match(
                    r".*net/img/(.*\.[jnpegif]{3,4})", image_url).group(1)
            except BaseException:
                print("The match fails, the rule is correct, pass ...")
            else:
                self.url_list.append(image_url)
                self.filename_list.append(image_filename)

    def image_url_match_verification(self, html):
        """图片地址匹配验证"""
        images1 = html.xpath("//a[@class='imgclasstag']")
        images2 = html.xpath("//a[@class='img imgclasstag']")
        if images1:
            self.image_url_match(images1)
        elif images2:
            self.image_url_match(images2)

    def getImageUrl_module(self):
        """采集图片地址模块"""
        for userInfo in userInfos:
            self.init_path(userInfo)
            time0 = time.time()
            if not self.check_file(self.image_url_path):
                files = os.listdir(self.html_path)
                self.url_list = []
                self.filename_list = []
                for file in files:
                    html = self.read_file(self.html_path + "{}".format(file))
                    html = etree.HTML(html)
                    self.image_url_match_verification(html)
                self.image_dict = dict(zip(self.filename_list, self.url_list))
                self.writ_file(self.image_url_path, self.image_dict)
            message = 'Task No.{userNo} [{blogNickName}] Get [imageURL.json] Success! run {time:.2f}'
            logger.info(message.format(**userInfo, time=time.time()-time0))

    def download(self):
        """下载图片模块"""
        for userInfo in userInfos:
            message = 'Task No.{userNo} [{blogNickName}] Download images'
            logger.info(message.format(**userInfo))
            self.init_path(userInfo)
            self.create_directory(self.image_path)
            t0 = time.time()
            count = self.download_many(userInfo)    # 多进程并行下载
            msg = '{} flags downloaded in {:.2f} seconds.'
            logger.info(msg.format(count, time.time() - t0))

    def download_one(self, image):
        '''下载一张图片
        :param image: 字典，包括图片的保存目录、图片的序号、图片的URL
        '''
        # message = 'Task No.{userNo} [{blogNickName}] Download No.{linkno} [{link}]'
        # logger.info(message.format(**image["userInfo"], **image))
        filename = os.path.split(image['link'])[1]
        if not self.check_file(self.image_path + filename):
            t0 = time.time()
            resp = requests.get(image['link'])
            with open(os.path.join(image['path'], filename), 'wb') as f:
                f.write(resp.content)
            t1 = time.time()
            message = 'Task No.{userNo} [{blogNickName}] Downloading No.{linkno} [{link}] run {time:.2f} seconds.'
            logger.info(message.format(**image["userInfo"], **image, time=t1-t0))

    def download_many(self, userInfo):
        '''多进程，按进程数 并行 下载所有图片
        使用concurrent.futures.ProcessPoolExecutor()
        Executor.map()使用Future而不是返回Future，它返回迭代器，
        迭代器的__next__()方法调用各个Future的result()方法，因此我们得到的是各个Future的结果，而非Future本身
        注意Executor.map()限制了download_one()只能接受一个参数，所以images是字典构成的列表
        '''
        with open(os.path.join(self.image_url_path)) as f:
            links = json.load(f).items()
        images = []
        for linkno, link in enumerate(links, 1):
            image = {
                'path': self.image_path,
                'linkno': linkno,
                'link': link[1],
                'userInfo': userInfo
            }
            images.append(image)
        # with语句将调用executor.__exit__()方法，
        # 而这个方法会调用executor.shutdown(wait=True)方法，它会在所有进程都执行完毕前阻塞主进程
        # 不指定max_workers时，进程池中进程个数默认为os.cpu_count()
        with futures.ProcessPoolExecutor(max_workers=16) as executor:
            # executor.map()效果类似于内置函数map()，但download_one()函数会在多个进程中并行调用
            # 它的返回值res是一个迭代器<itertools.chain object>，
            # 我们后续可以迭代获取各个被调用函数的返回值
            res = executor.map(self.download_one, images)  # 传一个序列
        return len(list(res))  # 如果有进程抛出异常，异常会在这里抛出，类似于迭代器中隐式调用next()的效果

    def rename_folder(self):
        """批量更改文件夹名"""
        files = os.listdir(self.g_parent_path)
        for userInfo in userInfos:
            for file in files:
                # （域名———>博客名）
                if userInfo['userDomain'] == file and userInfo["RenameFolder"] == 1:
                    old = self.g_parent_path + file
                    new = self.g_parent_path + "[博主]_" + userInfo['blogNickName']
                    os.rename(old, new)
                    logger.info("文件夹名：{}--->{}".format(file, "[博主]_" + userInfo['blogNickName']))
                # （博客名———>域名）
                elif "[博主]_" + userInfo['blogNickName'] == file and userInfo["RenameFolder"] == 0:
                    old = self.g_parent_path + file
                    new = self.g_parent_path + userInfo['userDomain']
                    os.rename(old, new)
                    logger.info("文件夹名：{}--->{}".format(file, userInfo['userDomain']))
                else:
                    pass

    def start(self):
        """运行爬虫"""
        # 文件夹重命名
        self.rename_folder()

        # 采集DWR-详情页URL模块
        self.getData_module()

        # 采集详情页html模块
        self.getPagesHtml_module()

        # 采集图片地址模块
        self.getImageUrl_module()

        # 下载图片模块
        self.download()


if __name__ == '__main__':
    loft = Loft()
    loft.start()