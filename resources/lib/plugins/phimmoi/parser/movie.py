# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.aes import CryptoAES
from utils.wisepacker import WisePacker
from urllib import unquote
from utils.mozie_request import Request, AsyncRequest
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

    def get_link(self, response, url, request):
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

        self.key
        if not self.key:
            return movie

        jsonresponse = re.search("_responseJson='(.*)';", response).group(1)
        jsonresponse = json.loads(jsonresponse.decode('utf-8'))

        # if jsonresponse['medias']:
        #     media = sorted(jsonresponse['medias'], key=lambda elem: elem['resolution'], reverse=True)
        #     for item in media:
        #         url = CryptoAES().decrypt(item['url'], bytes(self.key.encode('utf-8')))
        #         if not re.search('hls.phimmoi.net', url):
        #             movie['links'].append({
        #                 'link': url,
        #                 'title': 'Link %s' % item['resolution'],
        #                 'type': item['resolution'],
        #                 'resolve': False,
        #                 'originUrl': self.originURL
        #             })
        #         else:
        #             # hls.phimmoi.net
        #             movie['links'].append({
        #                 'link': url,
        #                 'title': 'Link hls',
        #                 'type': 'hls',
        #                 'resolve': False,
        #                 'originUrl': self.originURL
        #             })

        # if jsonresponse.get('embedUrls'):
        #     for item in jsonresponse.get('embedUrls'):
        #         url = self.get_url(CryptoAES().decrypt(item, bytes(self.key.encode('utf-8'))))
        #         if not re.search('hydrax', url):
        #             movie['links'].append({
        #                 'link': url,
        #                 'title': 'Link Unknow',
        #                 'type': 'mp4',
        #                 'resolve': False,
        #                 'originUrl': self.originURL
        #             })
        #         else:
        #             movie['links'].append({
        #                 'link': url,
        #                 'title': 'Link hydrax',
        #                 'type': 'hls',
        #                 'resolve': False,
        #                 'originUrl': self.originURL
        #             })

        if jsonresponse['thirdParty']:
            jobs = []
            self.key = "@@@3rd"
            for item in jsonresponse['thirdParty']:
                movie_url = self.get_url(CryptoAES().decrypt(item.get('embed'), bytes(self.key.encode('utf-8'))))
                if 'hydrax.html' not in movie_url:
                    movie['links'].append({
                        'link': movie_url,
                        'title': 'Link {}'.format(item.get('label', 'HD')),
                        'type': item.get('type'),
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

    def get_url(self, url):
        r = re.search(r'http://www.phimmoi.net/player.html\?v=1.00#url=(.*)', url)
        if r:
            return unquote(r.group(1))

        return url

    def parse_thirdparty_link(self, response, movie_links):
        source = re.search(r'var\sVIDEO_URL="(.*?)";', response)
        if source:
            movie_links.append({
                    'link': source.group(1),
                    'title': 'Link {}'.format('Third Party'),
                    'type': 'hls',
                    'resolve': False,
                    'originUrl': self.originURL
                })

        sources = re.search(r'var\slistFile=(\[.*?\]);', response)
        if sources:
            sources = json.loads(sources.group(1))
            for item in sources:
                movie_links.append({
                    'link': item.get('file'),
                    'title': 'Link {}'.format(item.get('label')),
                    'type': item.get('type'),
                    'resolve': False,
                    'originUrl': self.originURL
                })

        source = re.search(r'var\sVIDEO_URL=swapServer\("(.*)"\);', response)
        if source:
            movie_links.append({
                    'link': source.group(1),
                    'title': 'Link {}'.format('Third Party'),
                    'type': 'hls',
                    'resolve': False,
                    'originUrl': self.originURL
                })


