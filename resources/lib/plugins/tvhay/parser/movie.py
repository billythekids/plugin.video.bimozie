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
        servers = soup.select("div#servers > div.server")
        for server in servers:
            server_name = server.select_one('div.label').text.strip().encode('utf-8')
            if server_name != 'F.PRO:'.encode('utf-8'): continue
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.episodelist li a'):
                movie['group'][server_name].append({
                    'link': ep.get('href').encode('utf-8'),
                    'title': ep.get('title').encode('utf-8'),
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        sources = re.search("var sources = (\[{.*}\]);", response) \
                  or re.search("var sources[\s]?=[\s]?(\[{.*}\]);var", response)

        if sources is not None:
            sources = json.loads(sources.group(1))
            for source in sources:
                url = urllib.unquote(re.search('\?url=(.*)', source['file']).group(1))
                movie['links'].append({
                    'link': url,
                    'title': 'Link %s' % source['label'].encode('utf-8'),
                    'type': source['label'].encode('utf-8'),
                    'resolvable': False
                })

        return movie

