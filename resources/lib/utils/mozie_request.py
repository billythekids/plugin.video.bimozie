# -*- coding: utf-8 -*-
import urllib
import requests
from Queue import Queue
from threading import Thread


class Request:
    TIMEOUT = 45
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/59.0.3071.115 Safari/537.36"
    )
    DEFAULT_HEADERS = {
        'User-Agent': user_agent
    }
    session = None
    r = None

    def __init__(self, header=None, session=False):
        if header:
            self.DEFAULT_HEADERS = header
        if session:
            self.session = requests.session()

    def get(self, url, headers=None, params=None, redirect=True):
        print("Request URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.get(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                      allow_redirects=redirect)
        else:
            self.r = requests.get(url, headers=headers, timeout=self.TIMEOUT, params=params, allow_redirects=redirect)
        return self.r.text

    def post(self, url, params=None, headers=None, redirect=True):
        # print("Post URL: %s params: %s" % (url, urllib.urlencode(params)))
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.post(url, data=params, headers=headers, timeout=self.TIMEOUT,
                                       allow_redirects=redirect)
            for resp in self.r.history:
                print(resp.status_code, resp.url)
        else:
            self.r = requests.post(url, data=params, headers=headers, timeout=self.TIMEOUT, allow_redirects=redirect)
        return self.r.text

    def head(self, url, params=None, headers=None, redirect=True):
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.head(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                       allow_redirects=redirect)
        else:
            self.r = requests.head(url, headers=headers, timeout=self.TIMEOUT, params=params, allow_redirects=redirect)
        return self.r

    def options(self, url, params=None, headers=None, redirect=True):
        # if headers:
        #     headers = self.DEFAULT_HEADERS.update(headers)

        print(headers)
        if self.session:
            self.r = self.session.options(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                          allow_redirects=redirect)
        else:
            self.r = requests.options(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                      allow_redirects=redirect)
        return self.r

    def get_request(self):
        return self.r


class AsyncRequest:
    MIN_THREAD = 40
    RETRY = 1

    def __init__(self, request=None, retry=1):
        self.q = Queue(maxsize=0)
        self.request = request or Request()
        self.RETRY = retry

    def __create_queue(self, urls):
        print("*********************** Start Queue %d" % len(urls))
        self.num_theads = min(self.MIN_THREAD, len(urls))
        self.results = [{} for x in urls]
        for i in range(len(urls)):
            self.q.put((i, urls[i]))

    def __request(self, action, params=None, headers=None, redirect=False, parser=None, args=None):
        while not self.q.empty():
            work = self.q.get()
            retry = self.RETRY
            while retry > 0:
                try:
                    if action is 'head':
                        data = self.request.head(work[1], params, headers, redirect)
                    if action is 'get':
                        data = self.request.get(work[1], params, headers)
                    if action is 'post':
                        data = self.request.post(work[1], params, headers)
                    if parser:
                        data = parser(data, self.request, args)
                    # print('Requested %s' % work[1])
                    self.results[work[0]] = data
                    retry = 0
                except:
                    print('Request %s fail retry %d' % (work[1], retry))
                    self.results[work[0]] = {}
                    retry -= 1
            self.q.task_done()
        return True

    def head(self, urls, params=None, headers=None, redirect=False, parser=None, args=None):
        self.__create_queue(urls)

        for i in range(self.num_theads):
            worker = Thread(target=self.__request, args=('head', params, headers, redirect, parser, args))
            worker.setDaemon(True)
            worker.start()

        self.q.join()
        print("*********************** All %s thread done" % len(urls))
        return self.results

    def get(self, urls, headers=None, params=None, redirect=False, parser=None, args=None):
        self.__create_queue(urls)

        for i in range(self.num_theads):
            worker = Thread(target=self.__request, args=('get', params, headers, redirect, parser, args))
            worker.setDaemon(True)
            worker.start()

        self.q.join()
        print("*********************** All %s thread done" % len(urls))
        return self.results

    def post(self, urls, params, headers=None, redirect=False, parser=None, args=None):
        self.__create_queue(urls)

        for i in range(self.num_theads):
            worker = Thread(target=self.__request, args=('post', params, headers, redirect, parser, args))
            worker.setDaemon(True)
            worker.start()

        self.q.join()
        print("*********************** All %s thread done" % len(urls))
        return self.results
