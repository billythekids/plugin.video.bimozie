# -*- coding: utf-8 -*-
import urllib
import requests
import xbmcgui
from Queue import Queue
from threading import Thread


class Request:
    TIMEOUT = 45
    user_agent = (
        # "Mozilla/5.0 (X11; Linux x86_64) "
        # "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/59.0.3071.115 Safari/537.36"
    )
    DEFAULT_HEADERS = {
        'User-Agent': user_agent
    }
    session = None
    r = None

    def __init__(self, header=None, session=True):
        if header:
            self.DEFAULT_HEADERS = header
        if session:
            self.session = requests.session()

    def get(self, url, headers=None, params=None, redirect=True, cookies=None):
        print("Request URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.get(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                      allow_redirects=redirect, cookies=cookies)
        else:
            self.r = requests.get(url, headers=headers, timeout=self.TIMEOUT, params=params, allow_redirects=redirect,
                                  cookies=cookies)
        return self.r.text

    def post(self, url, params=None, headers=None, redirect=True, cookies=None):
        try: print("Post URL: %s params: %s" % (url, urllib.urlencode(params)))
        except: pass
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.post(url, data=params, headers=headers, timeout=self.TIMEOUT,
                                       allow_redirects=redirect, cookies=cookies)
            # for resp in self.r.history:
            #     print(resp.status_code, resp.url)
        else:
            self.r = requests.post(url, data=params, headers=headers, timeout=self.TIMEOUT, allow_redirects=redirect,
                                   cookies=cookies)
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
        if self.session:
            self.r = self.session.options(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                          allow_redirects=redirect)
        else:
            self.r = requests.options(url, headers=headers, timeout=self.TIMEOUT, params=params,
                                      allow_redirects=redirect)
        return self.r

    def get_request_session(self):
        return self.session

    def get_request(self):
        return self.r


class AsyncRequest:
    MIN_THREAD = 50
    RETRY = 1

    def __init__(self, request=None, retry=1):
        self.request = request or Request()
        self.RETRY = retry

    def __create_queue(self, urls):
        print("*********************** Start Queue %d" % len(urls))
        self.length = len(urls)
        self.q = Queue(maxsize=self.length)
        self.num_theads = min(self.MIN_THREAD, self.length)
        self.dialog = xbmcgui.DialogProgress()
        self.dialog.create('Get URL', "Loading 0/%d urls" % self.length)
        self.results = [{} for x in urls]
        for i in range(len(urls)):
            self.q.put((i, urls[i]))

    def __start_thread(self, args):
        for i in range(self.num_theads):
            worker = Thread(target=self.__request, args=args)
            worker.setDaemon(True)
            worker.start()

        self.q.join()
        print("*********************** All %s thread done" % self.length)
        self.dialog.close()

    def __request(self, action, params=None, headers=None, redirect=False, parser=None, args=None):
        while not self.q.empty():
            work = self.q.get()
            url = work[1]
            if type(url) is dict:
                params = 'params' in url and url['params'] or params
                headers = 'headers' in url and url['headers'] or headers
                redirect = 'redirect' in url and url['redirect'] or redirect
                parser = 'parser' in url and url['parser'] or parser
                args = 'args' in url and url['args'] or args
                url = work[1]['url']

            retry = self.RETRY
            while retry > 0:
                try:
                    if action is 'head':
                        data = self.request.head(url, params=params, headers=headers, redirect=redirect)
                    if action is 'get':
                        data = self.request.get(url, params=params, headers=headers)
                    if action is 'post':
                        data = self.request.post(url, params=params, headers=headers)
                    if parser:
                        data = parser(data, args)
                    # print('Requested %s' % work[1])
                    self.results[work[0]] = data
                    retry = 0
                except:
                    print('Request %s fail retry %d' % (work[1], retry))
                    self.results[work[0]] = {}
                finally:
                    retry -= 1

            done = self.q.qsize()
            progress = 100 - (done * 100 / self.length)
            self.dialog.update(progress, 'Processing %d/%d urls' % (self.length - done, self.length))
            self.q.task_done()
        return True

    def head(self, urls, params=None, headers=None, redirect=False, parser=None, args=None):
        self.__create_queue(urls)
        self.__start_thread(('head', params, headers, redirect, parser, args))
        return self.results

    def get(self, urls, headers=None, params=None, redirect=False, parser=None, args=None):
        self.__create_queue(urls)
        self.__start_thread(('get', params, headers, redirect, parser, args))
        return self.results

    def post(self, urls, params=None, headers=None, redirect=False, parser=None, args=None):
        self.__create_queue(urls)
        self.__start_thread(('post', params, headers, redirect, parser, args))
        return self.results
