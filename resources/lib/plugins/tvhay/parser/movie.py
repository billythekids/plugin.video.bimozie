# -*- coding: utf-8 -*-
import json
import re

from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from six.moves.urllib.parse import unquote


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
            server_name = py2_encode(server.select_one('div.label').text.strip())

            if not re.search('[SRB].PRO:', server_name): continue
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.episodelist li a'):
                movie['group'][server_name].append({
                    'link': py2_encode(ep.get('href')),
                    'title': py2_encode(ep.get('title'))
                })

        return movie

    def get_link(self, response, originURL):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        sources = re.search("var sources = (\[{.*}\]);", response) \
                  or re.search("var sources[\s]?=[\s]?(\[{.*}\]);var", response)

        if sources is not None:
            print(12313)
            return movie
            sources = json.loads(sources.group(1))
            for source in sources:
                url = unquote(re.search('\?url=(.*)', source['file']).group(1))
                movie['links'].append({
                    'link': url,
                    'title': 'Link %s' % py2_encode(source['label']),
                    'type': py2_encode(source['label']),
                    'originUrl': originURL,
                    'resolve': False
                })


        m = re.search('<iframe.*src="(.*?)"', response)
        if m is not None:
            source = unquote(m.group(1)).replace('\\', '')
            if source:
                if 'embedss.php?link=' in source:
                    source = re.search(r'embedss.php\?link=(.*)', source).group(1)

                movie['links'].append({
                    'link': source,
                    'title': py2_encode(source),
                    'type': 'Unknow',
                    'originUrl': originURL,
                    'resolve': False
                })

        return movie

