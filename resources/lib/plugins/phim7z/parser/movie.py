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

        source = re.search(r'iframe.*id=(.*?)\\?"', response)
        if source:
            # https://player.phim7z.tv/hls/getlink.php?id=d1FMYzZMVlkrdHRmOEZRamc5NTRNejhUYy85Rld5SG8vcmhUL2lIeHlEeU1UTXJLd0tiUkF5d0Q2emp3Z1hhaQ==
            response = json.loads(request.get(api_url % source.group(1)))
            Parser.create_link(movie['links'], response, domain)
            response = json.loads(request.get((api_url % source.group(1)) + '&type=hls'))
            Parser.create_link(movie['links'], response, domain)

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
