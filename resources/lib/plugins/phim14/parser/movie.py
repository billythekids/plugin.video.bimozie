# -*- coding: utf-8 -*-
import re
import json
import urllib
from bs4 import BeautifulSoup
from utils.mozie_request import Request
import utils.xbmc_helper as helper


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("ul#server_list > li.server_item")
        for server in servers:
            server_name = server.select_one('> strong')
            server_name = server_name.find(text=True, recursive=False)
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.episode_list li a'):
                movie['group'][server_name].append({
                    'link': ep.get('id'),
                    'title': 'Tập %s' % ep.text.encode('utf-8'),
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.search('<iframe.*src=".*?url=(.*?)"', response)
        if sources is not None:
            source = urllib.unquote(sources.group(1))
            movie['links'].append({
                'link': self.parse_link(source),
                'title': '',
                'type': '',
                'resolve': True
            })

        sources = re.search('<iframe.*src=(".*?")', response)
        if sources is not None:
            source = sources.group(1).replace('"', '')
            if source:
                movie['links'].append({
                    'link': self.parse_link(source),
                    'title': 'Link %s' % source,
                    'type': 'Unknow',
                    'resolve': False
                })

        sources = re.search('"sources": (.*),', response)
        if sources is not None:
            sources = json.loads(sources.group(1))
            if 'error' not in sources:
                if len(sources) > 1:
                    sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
                if len(sources) > 0:
                    for source in sources:
                        label = 'label' in source and source['label'] or ''
                        movie['links'].append({
                            'link': source['file'].replace('\\', ''),
                            'title': 'Link %s' % label.encode('utf-8'),
                            'type': label.encode('utf-8'),
                            'resolve': True
                        })

        return movie

    def remove_duplicate(self, items):
        movies = []
        for item in items:
            found = False
            for movie in movies:
                if movie['file'] == item['file']:
                    found = True
                    break
            if not found:
                movies.append(item)

        return movies

    def parse_link(self, url):
        r = re.search('stream.phim14.net/public/dist/index.html\?id=(.*)', url)
        if r:
            id = r.group(1)
            url = "http://stream.phim14.net/hls/%s/%s.playlist.m3u8" % (id, id)
            # res = Request().get(url)
            # abs_url = 'http://stream.phim14.net/hls/%s/drive/' % id
            # res = res.replace('/drive/', abs_url)
            url = helper.write_file('stream.strm', url)

        return url
