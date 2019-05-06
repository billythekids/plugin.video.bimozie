# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.aes import CryptoAES
from utils.wisepacker import WisePacker
import utils.xbmc_helper as helper
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get(self, response, url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        self.originURL = url

        try:
            error = soup.select_one('div.error-not-available div.alert-subheading').find(text=True, recursive=False).encode('utf-8')
            if error:
                helper.message(error, 'Not Found')
                return movie
        except: pass

        # get episode if possible
        servers = soup.select('div.list-server > div.server')
        if skipEps is False and len(servers) > 0:
            print("***********************Get Movie Episode*****************************")
            found = False
            items = self.get_server_list(servers)
            if items is not None and len(items) > 0:
                movie['group'] = items
                found = True
            else:
                found = False
            if found is False:
                servers = soup.select('ul.server-list > li.backup-server')
                movie['group'] = self.get_server_list(servers)

        else:
            movie['group']['phimmoi'] = [{
                'link': self.originURL,
                'title': 'Unknown link'
            }]

        return movie

    def get_link(self, response, url):
        print("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        self.originURL = url
        url = self.get_token_url(response)
        response = Request().get(url)

        self.key = self.get_decrypt_key(response)
        if not self.key:
            return movie

        jsonresponse = re.search("_responseJson='(.*)';", response).group(1)
        jsonresponse = json.loads(jsonresponse.decode('utf-8'))

        if jsonresponse['medias']:
            media = sorted(jsonresponse['medias'], key=lambda elem: elem['resolution'], reverse=True)
            for item in media:
                url = CryptoAES().decrypt(item['url'], bytes(self.key.encode('utf-8')))
                if not re.search('hls.phimmoi.net', url):
                    movie['links'].append({
                        'link': url,
                        'title': 'Link %s' % item['resolution'],
                        'type': item['resolution'],
                        'resolve': False,
                        'originUrl': self.originURL
                    })
                else:
                    # hls.phimmoi.net
                    movie['links'].append({
                        'link': url,
                        'title': 'Link hls',
                        'type': 'hls',
                        'resolve': False,
                        'originUrl': self.originURL
                    })
        elif jsonresponse['embedUrls']:
            for item in jsonresponse['embedUrls']:
                url = CryptoAES().decrypt(item, bytes(self.key.encode('utf-8')))
                if not re.search('hydrax', url):
                    movie['links'].append({
                        'link': url,
                        'title': 'Link Unknow',
                        'type': 'mp4',
                        'resolve': False,
                        'originUrl': self.originURL
                    })
                else:
                    movie['links'].append({
                        'link': url,
                        'title': 'Link hydrax',
                        'type': 'hls',
                        'resolve': False,
                        'originUrl': self.originURL
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
                        'title': episode.get('title').encode('utf-8')
                    })

        return items

    def get_decrypt_key(self, response):
        try:
            a = WisePacker.decode(response)
            return re.search("setDecryptKey\('(.*)'\);watching", a).group(1)
        except:
            helper.message(response, "Phimmoi", 15000)


    def get_token_url(self, response):
        a = WisePacker.decode(response)
        return re.search("'url':'(.*)','method'", a).group(1).replace("ip='+window.CLIENT_IP+'&", "")