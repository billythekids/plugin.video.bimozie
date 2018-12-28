# coding: utf8
from bs4 import BeautifulSoup
import re
import json
import urllib


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    key = "PhimMoi.Net@"

    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('a.btn-watch').get('href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.serverlist > div.server")
        for server in servers:
            server_name = server.select_one('div.label').find(text=True, recursive=False).strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.episodelist li a'):
                movie['group'][server_name].append({
                    'link': ep.get('data-episode-link'),
                    'title': ep.get('title').encode('utf-8'),
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        sources = re.search("<iframe .* src=\\\"(.*)\\\" frameborder", response)
        print(response)
        if sources is not None:
            print(sources.group(1))
        else:
            try:
                sources = json.loads(response)
                sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
                for source in sources:
                    movie['links'].append({
                        'link': source['file'],
                        'title': 'Link %s' % source['label'].encode('utf-8'),
                        'type': source['label'].encode('utf-8'),
                        'resolvable': True
                    })
                    if int(source['label'][0:-1]) >= 720: break
            except:
                pass

        return movie
