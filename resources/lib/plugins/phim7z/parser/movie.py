# -*- coding: latin1 -*-
from bs4 import BeautifulSoup
import re
import json


class Parser:
    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }

        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select('div.le-server')
        for server in servers:
            server_name = server.select_one(
                'div.les-title > strong').getText().strip().encode('utf8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('div.les-content > a'):
                movie['group'][server_name].append({
                    'link': ep.get('episode-id'),
                    'title': '%s' % ep.get('title').strip().encode('utf8'),
                })

        return movie

    def get_link(self, response, request, api_url, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        source = re.search(r'iframe.*src=\\"(.*?)\\"', response)
        if source:
            source = source.group(1).replace('\\', '')
            source = "https:{}".format(source)
            movie['links'].append({
                'link': source,
                'title': 'Link',
                'type': 'iframe',
                'resolve': False,
                'originUrl': domain
            })
            # https://player.phim7z.tv/hls/getlink.php?id=d1FMYzZMVlkrdHRmOEZRamc5NTRNejhUYy85Rld5SG8vcmhUL2lIeHlEeU1UTXJLd0tiUkF5d0Q2emp3Z1hhaQ==
            # response = request.get(source)
            # print response.encode('utf8')
            #
            # response = json.loads(response)
            # Parser.create_link(movie['links'], response, domain)
            # response = json.loads(request.get((api_url % source.group(1))))
            # Parser.create_link(movie['links'], response, api_url % source.group(1))

        return movie

    @staticmethod
    def create_link(links, response, domain):
        if response.get('status') is 1:
            sources = json.loads(response.get('data'))
            for f in sources:
                links.append({
                    'link': f.get('file'),
                    'title': 'Link %s' % f['label'],
                    'type': f['type'],
                    'resolve': False,
                    'originUrl': domain
                })
