# -*- coding: utf-8 -*-
import urllib
import requests


class Request:
    TIMEOUT = 30
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0'
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
