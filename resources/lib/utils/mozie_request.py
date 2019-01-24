# -*- coding: utf-8 -*-
import urllib
import requests


class Request:
    TIMEOUT = 30
    user_agent = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/59.0.3071.115 Safari/537.36"
    )
    DEFAULT_HEADERS = {
        'User-Agent': user_agent
    }
    session = None

    def __init__(self, header=None, session=False):
        if header:
            self.DEFAULT_HEADERS = header
        if session:
            self.session = requests.session()

    def get(self, url, headers=None):
        print("Request URL: %s" % url)
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            r = self.session.get(url, headers=headers)
        else:
            r = requests.get(url, headers=headers)
        return r.text

    def post(self, url, params, headers=None):
        print("Post URL: %s params: %s" % (url, urllib.urlencode(params)))
        if not headers:
            headers = self.DEFAULT_HEADERS
        if self.session:
            r = self.session.post(url, data=params, headers=headers)
            for resp in r.history:
                print(resp.status_code, resp.url)
        else:
            r = requests.post(url, data=params, headers=headers)
        return r.text
