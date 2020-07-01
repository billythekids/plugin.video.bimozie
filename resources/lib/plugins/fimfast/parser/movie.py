# -*- coding: utf-8 -*-
import re
import json
from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select('div#halim-list-server > div.halim-server')

        for server in servers:
            server_name = server.select_one('> span.halim-server-name').getText().strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.halim-list-eps > li'):
                if ep.select_one('a'):
                    ep = ep.select_one('a > span')
                else:
                    ep = ep.select_one('span')

                movie['group'][server_name].append({
                    'link': "{},{},{}".format(ep.get('data-episode-slug'),
                                              ep.get('data-server'),
                                              ep.get('data-post-id')),
                    'title': ep.get('data-episode-slug').encode('utf-8')
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = json.loads(response).get('data').get('sources')
        # print(sources.encode('utf8'))

        js_sources = re.search(r'sources:\s(\[.*?\])', sources).group(1)
        if js_sources and 'not-a-real-video-file' not in js_sources:
            js_sources = json.loads(js_sources)
            for s in js_sources:
                movie['links'].append({
                    'link': s.get('file'),
                    'title': 'Link {}'.format(s.get('label')),
                    'type': s.get('type'),
                    'resolve': False,
                    'originUrl': 'http://fimfast.tv',
                })

        source = re.search(r"<iframe.*src=\"(.*?)\"", sources)
        if source:
            source = source.group(1)
            if 'fimfast.com' not in source:
                movie['links'].append({
                    'link': source,
                    'title': 'Link Unknow',
                    'type': 'Unknow',
                    'resolve': False,
                    'originUrl': 'http://fimfast.tv',
                })

        return movie
