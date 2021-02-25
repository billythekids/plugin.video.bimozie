# -*- coding: utf-8 -*-
import json
import pickle
import re
import time

import utils.xbmc_helper as helper
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from utils.mozie_request import Request


class FShareVN:
    def __init__(self, url, username="", password=""):
        self.token = None
        self.url = url
        self.username = username
        self.password = password
        self.request = Request(session=True)
        # if helper.has_file_path('fshare.bin') and helper.get_last_modified_time_file('fshare.bin') + 43200 < int(
        #         time.time()):
        #     helper.remove_file('fshare.bin')
        #
        # if helper.has_file_path('fshare.bin'):
        #     with open(helper.get_file_path('fshare.bin')) as f:
        #         cache = pickle.load(f)
        #         self.request.get_request_session().cookies.set('session_id', cache.get('session_id'))

    @staticmethod
    def get_info(url=None, content=None):
        if url:
            content = Request().get(url)

        size = '0'
        soup = BeautifulSoup(content, "html.parser")
        title = py2_encode(soup.select_one('title').text)

        if 'Not Found' in title or '503' in title:
            raise Exception('Fshare', 'link die')

        elem = soup.select_one('form#form-download button#download-free')
        if elem:
            size = py2_encode(elem.text.strip() \
                              .replace(" ", "") \
                              .replace("\n", "") \
                              .replace("save", ""))
            size = re.search(r'\((.*?)\)', size).group(1)

        return title, size

    def login(self, token=""):
        url = 'https://api.fshare.vn/api/user/login'
        r = self.request.post(url, json={
            'user_email': self.username,
            'password': self.password,
            'app_key': 'L2S7R6ZMagggC5wWkQhX2+aDi467PPuftWUMRFSn'
        })

        r = json.loads(r)
        # if r.get('code') == 200:
        #     with open(helper.get_file_path('fshare.bin'), 'wb+') as f:
        #         pickle.dump(r, f)
        # else:
        #     helper.remove_file('fshare.bin')
        if r.get('code') != 200:
            raise Exception('Fshare', 'Login error')

        return r

    def get_user(self):
        url = 'https://api.fshare.vn/api/user/get'
        r = self.request.get(url)
        r = json.loads(r)
        if not r.get('id'):
            return False

        return r

    def get_token(self, url=None):
        if not self.token:
            data = self.login()
            cookie = data.get('session_id')
            self.request.get_request_session().cookies.set('session_id', cookie)
            self.token = data.get('token')
            if 'vip' not in self.get_user().get('account_type').lower():
                raise Exception('Fshare', 'Please login with your fshare vip account')

        return self.token, cookie

    def get_link(self):
        if re.search(r'/folder/([^\?]+)', self.url):
            code = self.handleFolder(self.url)
            if not code:
                return None
            else:
                self.url = "https://www.fshare.vn/file/%s" % code

        self.url = self.url.split("?")[0]
        token, session_id = self.get_token(self.url)

        r = self.request.post('https://api.fshare.vn/api/session/download', json={
            'token': token,
            'url': self.url
        })

        item = json.loads(r)

        # if 'errors' in item:
        #     helper.message("Fshare error: %s" % item['errors']['linkcode'][0])
        #     raise Exception('Fshare', 'error')
        #     return
        # # should block ui to wait until able retrieve a link
        # try:
        #     with self.request.get(item.get('location'), stream=True) as r:
        #         raise Exception('Fshare', 'found')
        # except Exception as ex:
        #     print ex
        # finally:
        #     self.logout()
        #     return item.get('location')

        if int(self.request.head(item.get('location')).headers['Content-Length']):
            self.request.head(item.get('location'))
            self.request.options(item.get('location'))
            self.logout(session_id)
            helper.message("Fshare link folder die")
            return item.get('location')
        return

    def logout(self, session_id):
        self.request.get('https://api.fshare.vn/api/user/logout/session_id={}'.format(session_id))

    @staticmethod
    def is_folder(url):
        return 'folder' in url and True or False

    def handleFolder(self, url=None, code=None, page=1):
        if not code:
            code = re.search(r'/folder/([^\?]+)', url).group(1)

        r = self.request.get('https://www.fshare.vn/api/v3/files/folder?linkcode=%s&sort=type,name&page=%s' % (code, page))
        r = json.loads(r)

        listitems = []
        if 'items' in r and len(r['items']) > 0:
            listitems = [("[%s] %s" % (i['type'] == 1 and helper.humanbytes(i["size"]) or 'Folder', i["name"]), i) for i in
                         r['items']]
        else:
            helper.message("Fshare link folder die")
            return

        last_page = page
        if r.get('_links').get('last'):
            last_page = re.search(r'&page=(\d+)', r.get('_links').get('last')).group(1)

        return listitems, int(last_page)

        # index = helper.create_select_dialog(listitems)
        # if index == -1: return None
        # if r['items'][index]['type'] == 1:
        #     return r['items'][index]['linkcode']
        # else:
        #     return self.handleFolder(code=r['items'][index]['linkcode'])
