# -*- coding: utf-8 -*-
import urllib
import requests


class Request:
    TIMEOUT = 15
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

    def get(self, url, headers=None, params=None):
        print("Request URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.get(url, headers=headers, timeout=self.TIMEOUT, params=params)
        else:
            self.r = requests.get(url, headers=headers, timeout=self.TIMEOUT, params=params)
        return self.r.text

    def post(self, url, params, headers=None):
        # print("Post URL: %s params: %s" % (url, urllib.urlencode(params)))
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            self.r = self.session.post(url, data=params, headers=headers, timeout=self.TIMEOUT)
            for resp in self.r.history:
                print(resp.status_code, resp.url)
        else:
            self.r = requests.post(url, data=params, headers=headers, timeout=self.TIMEOUT)
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

    def get_request(self):
        return self.r
