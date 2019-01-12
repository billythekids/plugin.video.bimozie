# coding: utf8
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.aes import CryptoAES
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    key = "PhimMoi.Net@"

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")

        # get episode if possible
        servers = soup.select('div.list-server > div.server')
        if skipEps is False and len(servers) > 0:
            print("***********************Get Movie Episode*****************************")
            found = False
            items = self.get_server_list(servers)
            if items is not None and len(items) > 0:
                movie['group'] = items
                found = True
            else: found = False
            if found is False:
                servers = soup.select('ul.server-list > li.backup-server')
                movie['group'] = self.get_server_list(servers)

        else:
            print("***********************Get Movie Link*****************************")
            url = self.get_token_url(response)
            response = Request().get(url)

            self.key = self.get_decrypt_key(response)
            jsonresponse = re.search("_responseJson='(.*)';", response).group(1)
            jsonresponse = json.loads(jsonresponse.decode('utf-8'))

            media = sorted(jsonresponse['medias'], key=lambda elem: elem['resolution'], reverse=True)
            for item in media:
                # if item['resolution'] <= 480: continue
                url = CryptoAES().decrypt(item['url'], bytes(self.key.encode('utf-8')))
                movie['links'].append({
                    'link': url,
                    'title': 'Link %s' % item['resolution'],
                    'type': item['resolution']
                })

        return movie

    def get_server_list(self, servers):
        items = {}
        for server in servers:
            if server.select_one('h3') is not None:
                server_name = server.select_one('h3').text.strip().replace("\n", "").encode('utf-8')
            else:
                return None

            if server_name not in items: items[server_name] = []

            if len(server.select('ul.list-episode li a')) > 0:
                for episode in server.select('ul.list-episode li a'):
                    items[server_name].append({
                        'link': episode.get('href'),
                        'title': episode.get('title').encode('utf-8'),
                    })

        return items

    def search_tokenize(self, response):
        m = re.search("eval\(.*\);}\('(.*)','(.*)','(.*)','(.*)'\)\);", response)
        a = self.decode_token(m.group(1), m.group(2), m.group(3), m.group(4))
        m = re.search("join\(''\);}\('(.*)','(.*)','(.*)','(.*)'\)\);$", a)
        a = self.decode_token(m.group(1), m.group(2), m.group(3), m.group(4))
        m = re.search("join\(''\);}\('(.*)','(.*)','(.*)','(.*)'\)\);$", a)
        a = self.decode_token(m.group(1), m.group(2), m.group(3), m.group(4))
        return a

    def get_decrypt_key(self, response):
        a = self.search_tokenize(response)
        return re.search("setDecryptKey\('(.*)'\);watching", a).group(1)

    def get_token_url(self, response):
        a = self.search_tokenize(response)
        return re.search("'url':'(.*)','method'", a).group(1).replace("ip='+window.CLIENT_IP+'&", "")

    def decode_token(self, w, i, s, e):
        a = 0
        b = 0
        c = 0
        string1 = []
        string2 = []
        string_len = len(w + i + s + e)

        while True:
            if a < 5:
                string2.append(w[a])
            else:
                if a < len(w):
                    string1.append(w[a])
            a += 1
            if b < 5:
                string2.append(i[b])
            else:
                if b < len(i):
                    string1.append(i[b])
            b += 1
            if c < 5:
                string2.append(s[c])
            else:
                if c < len(s):
                    string1.append(s[c])
            c += 1
            if string_len == len(string1) + len(string2) + len(e):
                break

        raw_string1 = ''.join(string1)
        raw_string2 = ''.join(string2)
        b = 0
        result = []
        for a in range(0, len(string1), 2):
            ll11 = -1
            if ord(raw_string2[b]) % 2: ll11 = 1
            part = raw_string1[a:a + 2]
            result.append(from_char_code(int(part, 36) - ll11))
            b += 1
            if b >= len(string2):
                b = 0

        return ''.join(result)
