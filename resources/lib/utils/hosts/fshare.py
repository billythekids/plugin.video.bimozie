# -*- coding: utf-8 -*-
import json
import pickle
import re
import time

from .. import xbmc_helper as helper
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from utils.mozie_request import Request


class FShareVN:
    api_url = 'https://api.fshare.vn/api'
    api_key = 'L2S7R6ZMagggC5wWkQhX2+aDi467PPuftWUMRFSn'
    api_app = ''

    def __init__(self, url="", username="", password=""):
        self.token = None
        self.url = url
        self.username = username
        self.password = password
        self.request = Request(session=True)
        self.current = int(time.time())

    def start_session(self):
        if helper.has_file_path('fshare.bin') \
                and helper.get_last_modified_time_file('fshare.bin') + 3600 < self.current:
            r = pickle.loads(helper.read_file('fshare.bin', True))
            helper.remove_file('fshare.bin')
            self.request.get_request_session().cookies.set('session_id', r.get('session_id'))
            try:
                self.logout()
            except:
                pass

        if helper.has_file_path('fshare.bin'):
            r = pickle.loads(helper.read_file('fshare.bin', True))
            self.request.get_request_session().cookies.set('session_id', r.get('session_id'))
            self.token = r.get('token')
        else:
            self.login()

        user = self.get_user()

    @staticmethod
    def is_folder(url):
        return 'folder' in url and True or False

    @staticmethod
    def get_info(url=None, content=None):
        if url:
            content = Request().get(url)

        size = '0'
        soup = BeautifulSoup(content, "html.parser")
        title = py2_encode(soup.select_one('title').text)
        title = title.replace('Fshare', '').replace(' - ', '')

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

    def login(self):
        helper.message('Login', 'Fshare')
        r = self.request.post('{}/user/login'.format(self.api_url), json={
            'user_email': self.username,
            'password': self.password,
            'app_key': self.api_key
        })

        r = json.loads(r)
        if r.get('code') == 200:
            helper.write_file('fshare.bin', pickle.dumps(r), True)
        else:
            helper.remove_file('fshare.bin')
            helper.message('Invalid user or password', 'Fshare Error')
            raise Exception('Login error', 'Fshare')

        # update session and token
        self.request.get_request_session().cookies.set('session_id', r.get('session_id'))
        self.token = r.get('token')

    def get_user(self):
        r = self.request.get('{}/user/get'.format(self.api_url))
        r = json.loads(r)
        if not r.get('id'):
            helper.message('Fshare login error', 'Error')
            raise Exception('Login error', 'Fshare')
        return r

    def get_my_favorite(self):
        self.start_session()
        r = self.request.get('{}/fileops/listFavorite'.format(self.api_url))
        r = json.loads(r)
        return r

    def get_link(self, url=None, code=None):
        self.url = url if url else self.url

        if self.is_folder(self.url):
            return None

        self.url = self.url if not code else "https://www.fshare.vn/file/%s" % code
        self.url = self.url.split("?")[0]

        self.start_session()
        r = self.request.post('{}/session/download'.format(self.api_url), json={
            'token': self.token,
            'url': self.url
        })

        item = json.loads(r)
        if int(self.request.head(item.get('location')).headers['Content-Length']) > 0:
            self.request.head(item.get('location'))
            self.request.options(item.get('location'))
            return item.get('location')
        return

    def logout(self):
        self.request.get('https://api.fshare.vn/api/user/logout')
        helper.remove_file('fshare.bin')

    def handleFolder(self, url=None, code=None, page=1):
        if not code:
            code = re.search(r'/folder/([^\?]+)', url).group(1)

        r = self.request.get(
            'https://www.fshare.vn/api/v3/files/folder?linkcode=%s&sort=type,name&page=%s' % (code, page))
        r = json.loads(r)

        listitems = []
        if 'items' in r and len(r['items']) > 0:
            listitems = [("[%s] %s" % (i['type'] == 1 and helper.humanbytes(i["size"]) or '', i["name"]), i) for i in
                         r['items']]
        else:
            helper.message("Fshare link folder die")

        last_page = page
        if r.get('_links').get('last'):
            last_page = re.search(r'&page=(\d+)', r.get('_links').get('last')).group(1)

        return listitems, int(last_page)

    def search(self, text):
        pass
