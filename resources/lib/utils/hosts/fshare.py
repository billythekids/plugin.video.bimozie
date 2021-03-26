# -*- coding: utf-8 -*-
import json
import pickle
import re
import time

from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from .. import xbmc_helper as helper
from ..mozie_request import Request, user_agent


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
                and helper.get_last_modified_time_file('fshare.bin') + 60 < self.current:
            r = pickle.loads(helper.read_file('fshare.bin', True))
            self.request.get_request_session().cookies.set('session_id', r.get('session_id'))
            self.logout()

        if helper.has_file_path('fshare.bin'):
            r = pickle.loads(helper.read_file('fshare.bin', True))
            self.request.get_request_session().cookies.set('session_id', r.get('session_id'))
            self.token = r.get('token')
        else:
            self.login()

        user = self.get_user()

    @staticmethod
    def extract_code(url):
        m = re.search(r'(file|folder)/([A-Z0-9]+)', url)
        return m.group(2)

    @staticmethod
    def get_asset_info(url=None, code=None, content=None):
        if not content:
            if url:
                is_folder, code = FShareVN.extract_code(url)
            content = Request().get('https://www.fshare.vn/api/v3/files/folder?linkcode=%s' % code)

        response = json.loads(content)
        return response.get('current').get('name'), \
               helper.humanbytes(response.get('current').get('size') if int(response.get('current').get('size')) > 0 else 0)

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
        # helper.message('Login success', 'Fshare')

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
        if 'location' in item:
            url = item.get('location')
            # url = helper.get_host_address_url(item.get('location'))
            # with self.request.get(url, stream=True) as r:
            #     r.raise_for_status()
            #     for chunk in r.iter_content(chunk_size=1024):
            #         return None
            helper.sleep(2000)
            return url

            return '{}|{}'.format(url, urlencode({
                'user-agent': user_agent,
                'verifypeer': 'true'
            }))
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
