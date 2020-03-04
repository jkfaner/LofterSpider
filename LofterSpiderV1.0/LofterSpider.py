# coding=utf-8
# /usr/bin/ python3

'''
Author:极客说_范儿
Email:geektalk@qq.com
Wechat & QQ:601872868

date:2020/2/8 1:18 上午
dese:LofterSpider V1.0
'''

import sys
import re
import time
from tqdm import tqdm
import traceback
import requests
import os
import json
from lxml import etree


class SpiderMethod(object):

    def __init__(self, config):
        self.g_parent_path = os.path.split(os.path.realpath(__file__))[
            0] + os.sep + "Loft资源/"
        self.user_info_list = config['user_id_list']
        self.parent_path = ''
        self.archive_html_path = ''
        self.dwr_path = ''
        self.url_path = ''
        self.html_path = ''
        self.image_path = ''
        self.user_info = ''
        self.image_url_path = ''
        self.image_url = ''
        self.image_filename = ''
        self.user_id = ''
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
            with open(path, 'a') as f:
                f.write(data)
        elif isinstance(data, dict):
            with open(path, 'w') as f:
                f.write(json.dumps(data, ensure_ascii=False))

    @staticmethod
    def read_file(path):
        """读取目录下的文件"""
        with open(path, 'r') as f:
            data = f.read()
            return data

    def get_id(self, html):
        """获取用户归档页用户id"""
        user_id_list = html.xpath("//iframe[@id='control_frame']")
        for user_id in user_id_list:
            user_id = re.search(
                "blogId=([0-9]*)",
                user_id.attrib['src']).group(1)
            self.user_id = user_id


class Loft(SpiderMethod):
    """乐乎个人爬虫"""

    def dwr_headers(self, user_id):
        """初始化headers"""
        url = 'http://%s.lofter.com/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr' % self.user_info
        self.payload = {
            "callCount": "1",
            "scriptSessionId": "${scriptSessionId}187",
            "httpSessionId": "",
            "c0-scriptName": "ArchiveBean",
            "c0-methodName": "getArchivePostByTime",
            "c0-id": "0",
            "c0-param0": "boolean:false",
            "c0-param1": "number:%s" % user_id,
            "c0-param3": "number:50",
            "c0-param4": "boolean:false",
            "batchId": "1"}
        self.headers = {
            "Content-Type": "text/plain",
            'Referer': 'https://%s.lofter.com/view' % self.user_info,
            "Host": "%s.lofter.com" % self.user_info,
            "Origin": "https://%s.lofter.com" % self.user_info,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, "
            "like Gecko) Chrome/79.0.3945.79 Safari/537.36 ",
        }
        return url

    def get_dwr(self, url):
        """获取dwr"""
        time.sleep(0.1)
        dwr = requests.post(url, data=self.payload, headers=self.headers).text
        return dwr

    def error(self):
        print("\n\nHTTP ERROR 403\n访问 %s.lofter.com 的请求遭到拒绝\n原因：\n"
              "1.你的IP可能被列入网站黑名单\n"
              "2.你可能被限制访问该路径下的文件\n"
              "3.服务器繁忙，同一IP地址发送请求过多，可能遭到服务器智能屏蔽\n...\n"
              "[ 程序强制退出... ]\n\n" % self.user_info)
        quit()

    def init_path(self, user_info):
        """初始化文件（夹）路径"""
        self.parent_path = self.g_parent_path + "%s/" % user_info
        self.archive_html_path = self.parent_path + "归档页.html"
        self.dwr_path = self.parent_path + "DWR.txt"
        self.url_path = self.parent_path + "htmlURL.json"
        self.html_path = self.parent_path + "html/"
        self.image_path = self.parent_path + "img/"
        self.user_info = user_info
        self.image_url_path = self.parent_path + "imageURL.json"

    def write_html(self):
        url = "https://%s.lofter.com/view" % self.user_info
        try:
            time.sleep(0.5)
            html = self.get_html(url)
        except Exception as e:
            print("%s\n" % e)
            self.error()
        else:
            self.writ_file(self.archive_html_path, html)

    def write_permalink_dict(self, permalinks):
        """匹配详情页面url"""
        url_list = []
        for permalink in permalinks:
            # 匹配url
            url = "https://%s.lofter.com/post/%s" % (
                self.user_info, permalink)
            url_list.append(url)
        permalink_dict = {
            permalink: url for permalink, url in zip(
                permalinks, url_list)}
        self.writ_file(self.url_path, permalink_dict)

    def get_new_dwr(self, url):
        """获取最新dwr"""
        self.payload["c0-param2"] = "number:%s" % str(time.time() * 1000)[:13]
        dwr = self.get_dwr(url)
        with open(self.dwr_path, 'w') as f:
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
            except BaseException:
                print("未采集到dwr数据 或 用户未发表图片")
            else:
                self.payload["c0-param2"] = "number:%s" % time_list[-1]
                dwr = self.get_dwr(url)
                self.writ_file(self.dwr_path, dwr)

    def collection_details_page_url_module(self):
        """采集归档页html-DWR-详情页URL"""
        for user_info in self.user_info_list:
            self.init_path(user_info)
            self.create_directory(self.g_parent_path)
            self.create_directory(self.parent_path)
            print("\n----开始获取%s-【归档页】-【DWR】-【详情页URL】----" % self.user_info)

            if not self.check_file(self.archive_html_path):
                self.write_html()
            html = self.read_file(self.archive_html_path)
            html = etree.HTML(html)
            try:
                self.get_id(html)
            except BaseException:
                print("再次获取html及id")
                self.write_html()
                html = self.read_file(self.archive_html_path)
                html = etree.HTML(html)
                self.get_id(html)
            else:
                pass

            print("\n开始采集dwr...")
            url = self.dwr_headers(self.user_id)
            self.get_new_dwr(url)
            self.get_other_dwr(url)

            print("\n获取详情页面url...")
            dwr = self.read_file(self.dwr_path)
            permalinks = re.findall("""permalink="([0-9a-z_]*)";""", dwr)
            # 检查是否有文件存在
            if not self.check_file(self.url_path):
                self.write_permalink_dict(permalinks)
            # 验证数据完整性
            if not len(json.load(open(self.url_path))) == len(permalinks):
                print("数据不完整...再次采集...")
                self.write_permalink_dict(permalinks)

            print("%s :\n【归档页html】\n【DWR】\n【详情页URL】\n全部获取成功！" % user_info)

    def collection_all_page_html_module(self):
        """采集详情页html"""
        for user_info in self.user_info_list:
            print("\n---开始获取%s详情页面HTML---\n读取htmlURL.json..." % user_info)
            self.init_path(user_info)
            url_dict = json.load(open(self.url_path))
            self.create_directory(self.html_path)
            for permalink, url in tqdm(url_dict.items()):
                if not self.check_file(self.html_path + "%s.html" % permalink):
                    try:
                        time.sleep(0.5)
                        html = self.get_html(url).decode("utf-8")
                    except Exception as e:
                        print("%s\n" % e)
                        self.error()
                    else:
                        self.writ_file(
                            self.html_path + "%s.html" %
                            permalink, html)
                else:
                    pass
            print("\n%s :\n【详情页面URL-%s.json】\n获取成功！" % (user_info, user_info))

    def image_url_match(self, images):
        """图片地址匹配"""
        for image in images:
            try:
                self.image_url = re.search(
                    r"(.*net/img/.*\.[jnpegif]{3,4})?",
                    image.attrib['bigimgsrc']).group(1)
                self.image_filename = re.match(
                    r".*net/img/(.*\.[jnpegif]{3,4})", self.image_url).group(1)
            except BaseException:
                print("匹配失败，正则无误，pass...")
            else:
                self.url_list.append(self.image_url)
                self.filename_list.append(self.image_filename)

    def image_url_match_verification(self, html):
        """图片地址匹配验证"""
        # 如果匹配地址出错，可添加更多规则
        images1 = html.xpath("//a[@class='imgclasstag']")
        images2 = html.xpath("//a[@class='img imgclasstag']")
        print(type(images1))
        if images1:
            self.image_url_match(images1)
        elif images2:
            self.image_url_match(images2)

    # 采集图片地址模块
    def capture_picture_address_module(self):
        for user_info in self.user_info_list:
            print("\n---开始获取%s图片地址---" % user_info)
            self.init_path(user_info)
            if not self.check_file(self.image_url_path):
                files = os.listdir(self.html_path)
                self.url_list = []
                self.filename_list = []
                for file in tqdm(files):
                    html = self.read_file(self.html_path + "%s" % file)
                    html = etree.HTML(html)
                    self.image_url_match_verification(html)
                self.image_dict = {
                    filename: url for filename, url in zip(
                        self.filename_list, self.url_list)}
                self.writ_file(self.image_url_path, self.image_dict)
            print("\n%s :\n【图片url-%s.json】\n获取成功！" % (user_info, user_info))

    def ini_download(self):
        """下载图片模块"""
        for user_info in self.user_info_list:
            print("\n---开始下载%s图片---" % user_info)
            self.init_path(user_info)
            self.create_directory(self.image_path)
            self.url_dict = json.load(open(self.image_url_path))
            start = time.time()

            # 1.单进程
            for filename, url in tqdm(self.url_dict.items()):
                if not self.check_file(self.image_path + filename):
                    self.download(url, filename)
            end = time.time()
            print("进程（ %s） runs %0.2f seconds." % (os.getpid(), (end - start)))
        print("\n%s 图片下载完毕..." % self.user_info)

    def download(self, url, filename):
        self.url = url
        # .jpg .jpeg .gif .png
        if filename[-4] == 'j':
            self.url = url + "g"
        try:
            image = self.get_html(self.url)
        except Exception as e:
            print("%s\n" % e)
            self.error()
        else:
            self.writ_file(self.image_path + filename, image)

    def start(self):
        """运行爬虫"""
        print("=" * 100)
        # 归档页html-DWR-详情页URL
        self.collection_details_page_url_module()

        # 采集详情页html模块
        self.collection_all_page_html_module()

        # 采集图片地址模块
        self.capture_picture_address_module()

        # 下载图片模块
        self.ini_download()


def main():
    try:
        config_path = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'config.json'
        if not os.path.isfile(config_path):
            sys.exit(u'当前路径：%s 不存在配置文件config.json' %
                     (os.path.split(os.path.realpath(__file__))[0] + os.sep))
        with open(config_path) as f:
            config = json.loads(f.read())
        loft = Loft(config)
        loft.start()
    except ValueError:
        print(u'config.json 格式不正确.')
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
