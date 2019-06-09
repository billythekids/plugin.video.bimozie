# -*- coding: utf-8 -*-
import re
import json
import utils.xbmc_helper as helper
from utils.mozie_request import Request


class FShare:
    def __init__(self, url, username="", password=""):
        self.url = url
        self.username = username
        self.password = password
        self.request = Request(session=True)

    def login(self, token):
        url = 'https://www.fshare.vn/site/login'
        r = self.request.post(url, {
            '_csrf-app': token,
            'LoginForm[email]': self.username,
            'LoginForm[password]': self.password,
            'LoginForm[rememberMe]': 1
        })

        return r

    def get_token(self):
        r = self.request.get('https://www.fshare.vn/')
        if not re.search(r'id="form-signup"', r):
            print('Fashare: already login')
            return self.extract_token(r)
        else:
            print('Fashare: try to login')
            r = self.login(self.extract_token(r))
            return self.extract_token(r)

    def extract_token(self, response):
        return re.search(r'name="csrf-token" content="(.*)">', response).group(1)

    def get_link(self):
        token = self.get_token()
        code = re.search(r'/file/([^\?]+)', self.url).group(1)

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
