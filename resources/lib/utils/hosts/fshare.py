# -*- coding: utf-8 -*-
import urllib, pickle, time, json, re
import utils.xbmc_helper as helper
from utils.mozie_request import Request
from bs4 import BeautifulSoup


class FShareVN:
    def __init__(self, url, username="", password=""):
        self.token = None
        self.url = url
        self.username = username
        self.password = password
        self.request = Request(session=True)
        if helper.has_file_path('fshare.bin') and helper.get_last_modified_time_file('fshare.bin') + 43200 < int(
                time.time()):
            helper.remove_file('fshare.bin')

        if helper.has_file_path('fshare.bin'):
            with open(helper.get_file_path('fshare.bin')) as f:
                cache = pickle.load(f)
                self.request.get_request_session().cookies.set('session_id', cache.get('session_id'))

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

            size = info.select_one('div.size').get_text().strip() \
                .replace(" ", "") \
                .replace("\n", "") \
                .replace("save", "").encode('utf-8')

        return name, size

    def login(self, token=""):
        url = 'https://api.fshare.vn/api/user/login'
        r = self.request.post(url, json={
            'user_email': self.username,
            'password': self.password,
            'app_key': 'L2S7R6ZMagggC5wWkQhX2+aDi467PPuftWUMRFSn'
        })

        r = json.loads(r)
        if r.get('code') == 200:
            with open(helper.get_file_path('fshare.bin'), 'wb+') as f:
                pickle.dump(r, f)
        else:
            helper.remove_file('fshare.bin')
            raise Exception('Fshare', 'Login error')

        return r

    def get_user(self):
        url = 'https://api.fshare.vn/api/user/get'
        r = self.request.get(url)
        print r
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

        return self.token

    def get_link(self):
        if re.search(r'/folder/([^\?]+)', self.url):
            code = self.handleFolder(self.url)
            if not code:
                return None
            else:
                self.url = "https://www.fshare.vn/file/%s" % code

        self.url = self.url.split("?")[0]
        token = self.get_token(self.url)

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
            # self.logout()
            helper.sleep(3000)
            return item.get('location')
        return

    def logout(self):
        self.request.get('https://api.fshare.vn/api/user/logout')

    @staticmethod
    def is_folder(url):
        return not re.search(r'/folder/([^\?]+)', url) and False or True

    def handleFolder(self, url=None, code=None):
        if not code:
            code = re.search(r'/folder/([^\?]+)', url).group(1)

        r = self.request.get('https://www.fshare.vn/api/v3/files/folder?linkcode=%s&sort=type,name' % code)
        r = json.loads(r)

        listitems = []
        if 'items' in r and len(r['items']) > 0:
            listitems = ["[%s] %s" % (i['type'] == 1 and helper.humanbytes(i["size"]) or 'Folder', i["name"]) for i in
                         r['items']]
        else:
            helper.message("Fshare link folder die")
            return

        index = helper.create_select_dialog(listitems)
        if index == -1: return None
        if r['items'][index]['type'] == 1:
            return r['items'][index]['linkcode']
        else:
            return self.handleFolder(code=r['items'][index]['linkcode'])
