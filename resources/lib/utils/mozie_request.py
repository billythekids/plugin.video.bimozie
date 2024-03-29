# -*- coding: utf-8 -*-
import traceback

import requests
import xbmcgui
import time
import concurrent.futures
from . import xbmc_helper as helper
# import requests_cache
# requests_cache.install_cache(helper.REQUEST_CACHE, backend='sqlite', expire_after=604800)

try:
    from queue import Queue
except ImportError:
    import Queue

from threading import Thread

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/86.0.4240.75 Safari/537.36"
)


class Request:
    TIMEOUT = 60

    DEFAULT_HEADERS = {
        'user-agent': user_agent,
    }
    session = None
    r = None

    def __init__(self, header=None, session=True, cookies=None):
        if header:
            self.DEFAULT_HEADERS = header
        if session:
            self.session = requests.session()
        if cookies:
            self.session = requests.session()
            self.session.cookies.update(cookies)

    def get(self, url, headers=None, params=None, redirect=True, cookies=None, verify=True, stream=False):
        helper.log("Request URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS

        if self.session:
            self.r = self.session.get(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                      allow_redirects=redirect, cookies=cookies, verify=verify, stream=stream)
        else:
            self.r = requests.get(url, headers=headers, timeout=self.TIMEOUT, params=params, allow_redirects=redirect,
                                  cookies=cookies, stream=stream)

        # helper.log("---------------- Encoding ----------------")
        # helper.log(self.r.encoding)
        # helper.log("---------------- -------- ----------------")
        if stream:
            return self.r
        return self.r.text

    def post(self, url, params=None, headers=None, redirect=True, cookies=None, json=None, verify=True, data=None):
        helper.log("Post URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS

        if self.session:
            self.r = self.session.post(url, data=params, headers=headers, timeout=self.TIMEOUT,
                                       allow_redirects=redirect, cookies=cookies, json=json, verify=verify)
            # for resp in self.r.history:
            #     helper.log(resp.status_code, resp.url)
        else:
            self.r = requests.post(url, data=params, headers=headers, timeout=self.TIMEOUT, allow_redirects=redirect,
                                   cookies=cookies, json=json)
        return self.r.text

    def head(self, url, params=None, headers=None, redirect=True, cookies=None, verify=True):
        helper.log("Head URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS

        if self.session:
            self.r = self.session.head(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                       allow_redirects=redirect, verify=verify)
        else:
            self.r = requests.head(url, headers=headers, timeout=self.TIMEOUT, params=params, allow_redirects=redirect)
        return self.r

    def options(self, url, params=None, headers=None, redirect=True, cookies=None, verify=True):
        helper.log("Options URL: %s" % url)
        # if headers:
        #     headers = self.DEFAULT_HEADERS.update(headers)
        if self.session:
            self.r = self.session.options(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                          allow_redirects=redirect, verify=verify)
        else:
            self.r = requests.options(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                      allow_redirects=redirect)
        return self.r

    def set_session(self, session):
        self.session = session

    def get_request_session(self):
        return self.session

    def get_request(self):
        return self.r


class AsyncRequest:
    MIN_THREAD = 50
    RETRY = 1

    def __init__(self, request=None, retry=1, thread=50, delay=0):
        self.request = request or Request()
        self.RETRY = retry
        self.MIN_THREAD = thread
        self.Delay = delay

    def __create_queue(self, urls):
        helper.log("*********************** Start Queue %d" % len(urls))
        self.length = len(urls)
        self.q = Queue(maxsize=self.length)
        self.num_theads = min(self.MIN_THREAD, self.length)
        self.dialog = xbmcgui.DialogProgress()
        self.dialog.create('Get URL', "Loading 0/%d urls" % self.length)
        self.results = [{} for x in urls]
        for i in range(len(urls)):
            self.q.put((i, urls[i]))

    def __start_thread(self, *args):
        start_time = time.time()
        for i in range(self.num_theads):
            worker = Thread(target=self.__request, args=args)
            worker.setDaemon(True)
            worker.start()

        self.q.join()
        self.dialog.close()
        helper.log("*********************** All %s threads done in %s" % (self.length, time.time() - start_time))

    def __request(self, action, params=None, headers=None, redirect=False, parser=None, args=None, json=None,
                  cookies=None, verify=True):
        helper.log("params {}, headers {}, json: {}, redirect {}, cookies {}, verify {}" \
              .format(params, headers, json, redirect, cookies, verify))

        while not self.q.empty():
            work = self.q.get()
            url = work[1]
            required_response_header = False
            data = None
            if type(url) is dict:
                if url.get('params'): params = url.get('params')
                if url.get('headers'): headers = url.get('headers')
                if url.get('redirect'): redirect = url.get('redirect')
                if url.get('parser'): parser = url.get('parser')
                if url.get('args'): args = url.get('args')
                if url.get('json'): json = url.get('json')
                if url.get('cookies'): cookies = url.get('cookies')
                if url.get('responseHeader'): required_response_header = True
                if url.get('verify') is False: verify = False
                url = work[1]['url']

            retry = self.RETRY
            helper.log("url {}, params {}, headers {}, json: {}, redirect {}, cookies {}, verify {}, required_header {}" \
                  .format(url, params, headers, json, redirect, cookies, verify, required_response_header))

            while retry > 0:
                try:
                    if action == 'head':
                        data = self.request.head(url, params=params, headers=headers, redirect=redirect,
                                                 cookies=cookies, verify=verify)
                    if action == 'get':
                        data = self.request.get(url, params=params, headers=headers, redirect=redirect, cookies=cookies,
                                                verify=verify)
                    if action == 'post':
                        data = self.request.post(url, params=params, headers=headers, json=json, redirect=redirect,
                                                 cookies=cookies, verify=verify)
                    if parser:
                        if required_response_header:
                            response_headers = self.request.get_request().headers
                            data = parser(data, args, response_headers)
                        else:
                            data = parser(data, args)
                    helper.log('Async Requested %s' % work[1])
                    self.results[work[0]] = data
                    retry = 0
                    time.sleep(self.Delay)

                except Exception as inst:
                    # helper.log(inst)
                    helper.log('Async Request %s fail retry %d' % (work[1], retry))
                    # traceback.print_exc()
                    self.results[work[0]] = {}
                finally:
                    retry -= 1

            done = self.q.qsize()
            progress = int(100 - (done * 100 / self.length))
            self.dialog.update(progress, 'Processing %d/%d urls' % (self.length - done, self.length))
            self.q.task_done()

        return True

    def head(self, urls, params=None, headers=None, redirect=False, parser=None, args=None, cookies=None, verify=True):
        self.__create_queue(urls)
        self.__start_thread('head', params, headers, redirect, parser, args, None, cookies, verify)
        return self.results

    def get(self, urls, headers=None, params=None, redirect=True, parser=None, args=None, cookies=None, verify=True):
        self.__create_queue(urls)
        self.__start_thread('get', params, headers, redirect, parser, args, None, cookies, verify)
        return self.results

    def post(self, urls, params=None, headers=None, json=None, redirect=False, parser=None, args=None, cookies=None,
             verify=True):
        self.__create_queue(urls)
        self.__start_thread('post', params, headers, redirect, parser, args, json, cookies, verify)
        return self.results
