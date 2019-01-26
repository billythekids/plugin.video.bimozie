# -*- coding: utf-8 -*-
import re
import json
import utils.xbmc_helper as helper
from utils.mozie_request import Request


class FShare:
    def __init__(self, url, username="", password=""):
        self.request = Request(session=True)
        self.url = url
        self.username = username
        self.password = password

    def login(self):
        token = self.get_token()
        code = self.url.replace('https://www.fshare.vn', '')
        url = 'https://www.fshare.vn/site/login?backUrl=%s' % code
        r = self.request.post(url, {
            '_csrf-app': token,
            'LoginForm[email]': self.username,
            'LoginForm[password]': self.password,
            'LoginForm[rememberMe]': 1
        })

        return r

    def get_token(self):
        r = self.request.get(self.url)
        return self.extract_token(r)

    def extract_token(self, response):
        return re.search('name="csrf-token" content="(.*)">', response).group(1)

    def get_link(self):
        if not self.username or not self.password:
            token = self.get_token()
        else:
            r = self.login()
            token = self.extract_token(r)

        code = re.search('/file/([^\?]+)', self.url).group(1)

        r = self.request.post('https://www.fshare.vn/download/get', {
            '_csrf-app': token,
            'linkcode': code,
            'withFcode5': 0,
            'fcode': ''
        })

        item = json.loads(r)
        # self.logout()
        if 'errors' in item:
            helper.message("Fshare error: %s" % item['errors']['linkcode'][0])
            raise Exception('Fshare', 'error')
            return
        # should block ui to wait until able retrieve a link
        return item[u'url']

    def logout(self):
        self.request.get('https://www.fshare.vn/site/logout')
