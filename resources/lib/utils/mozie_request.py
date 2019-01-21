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

    def get(self, url):
        print("Request URL: %s" % url)
        if self.session:
            r = self.session.get(url, headers=self.DEFAULT_HEADERS)
        else:
            r = requests.get(url, headers=self.DEFAULT_HEADERS)
        return r.text

    def post(self, url, params):
        print("Post URL: %s params: %s" % (url, urllib.urlencode(params)))
        if self.session:
            r = self.session.post(url, data=params, headers=self.DEFAULT_HEADERS)
            for resp in r.history:
                print(resp.status_code, resp.url)
        else:
            r = requests.post(url, data=params, headers=self.DEFAULT_HEADERS)
        return r.text
