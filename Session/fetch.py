#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project:
@File: fetch.py
@Ide: PyCharm
@Time: 2021-05-29 13:53:43
@Desc: request请求
"""
from random import choice

import requests
from requests import Response
from retrying import retry
from util.logger import logger

retry_max_number = 10
retry_min_random_wait = 1000
retry_max_random_wait = 30000
fetch_timeout = 30000

User_Agent_List = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
]
User_Agent = User_Agent_List[0]


class Session(object):

    def __init__(self):
        self.session = requests.session()

    def __need_retry(self, exception):
        result = isinstance(exception, (requests.ConnectionError, requests.ReadTimeout))
        if result:
            logger.warning(f'Exception: {type(exception)} occurred, retrying...')
        return result

    def __init_request_headers(self, session, **kwargs):
        session.headers.update({'User-Agent': choice(User_Agent_List)})
        return session, kwargs

    def __fetch(self, session, url, method='get', check_code=True, **kwargs):

        @retry(stop_max_attempt_number=retry_max_number, wait_random_min=retry_min_random_wait,
               wait_random_max=retry_max_random_wait, retry_on_exception=self.__need_retry)
        def _fetch(session, url, check_code, **kwargs) -> Response:
            response = session.post(url, **kwargs) if method == 'post' else session.get(url, **kwargs)
            if check_code:
                if response.status_code != 200:
                    error_info = f'Expected status code 200, but got {response.status_code}.'
                    raise requests.ConnectionError(error_info)
            return response

        try:
            session, kwargs = self.__init_request_headers(session, **kwargs)
            resp = _fetch(session, url, check_code, **kwargs)
            return resp
        except Exception as e:
            error_info = 'Something got wrong, error msg:{}'.format(e)
            raise Exception(error_info)

    def fetch(self, url, headers=None, method='get', session=None, **kwargs):
        session = self.session if session is None else session
        resp = self.__fetch(session=session, url=url, method=method, headers=headers, **kwargs)
        return resp

    def fetch_json(self, url, headers=None, method='get', session=None, **kwargs):
        resp = self.fetch(url, headers, method, session, **kwargs)
        return resp.json()
