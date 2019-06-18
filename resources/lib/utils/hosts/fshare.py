# -*- coding: utf-8 -*-
import re
import json
import utils.xbmc_helper as helper
from utils.mozie_request import Request
from bs4 import BeautifulSoup


class FShareVN:
    def __init__(self, url, username="", password=""):
        self.url = url
        self.username = username
        self.password = password
        self.request = Request(session=True)

    @staticmethod
    def get_info(url=None, content=None):
        if url:
            content = Request().get(url)

        name = False
        size = '0'
        soup = BeautifulSoup(content, "html.parser")
        title = soup.select_one('title').text.encode('utf-8')

        if 'Not Found' in title or '503' in title:
            raise Exception('Fshare', 'link die')

        info = soup.select_one('div.info')
        if info:
            name = info.select_one('div.name').get('title').encode('utf-8')
            print(name)

            size = info.select_one('div.size').get_text().strip()\
                .replace(" ", "")\
                .replace("\n", "")\
                .replace("save", "").encode('utf-8')

        return name, size

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
        if re.search(r'/folder/([^\?]+)', self.url):
            code = self.handleFolder(self.url)
            if not code:
                return None
        else:
            code = re.search(r'/file/([^\?]+)', self.url).group(1)

        token = self.get_token()

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

    def is_folder(self, url):
        return not re.search(r'/folder/([^\?]+)', url) and False or True

    def handleFolder(self, url=None, code=None):
        if not code:
            code = re.search(r'/folder/([^\?]+)', url).group(1)

        r = self.request.get('https://www.fshare.vn/api/v3/files/folder?linkcode=%s&sort=type,name' % code)
        r = json.loads(r)

        listitems = []
        if 'items' in r and len(r['items']) > 0:
            listitems = ["[%s] %s" % (i['type'] == 1 and helper.humanbytes(i["size"]) or 'Folder', i["name"]) for i in r['items']]
        else:
            raise Exception('Fshare', 'link die')

        index = helper.create_select_dialog(listitems)
        if index == -1: return None
        if r['items'][index]['type'] == 1:
            return r['items'][index]['linkcode']
        else:
            return self.handleFolder(code=r['items'][index]['linkcode'])


