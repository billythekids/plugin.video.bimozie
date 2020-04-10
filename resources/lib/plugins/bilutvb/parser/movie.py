# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
import json
from utils.mozie_request import Request


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
            episodes = server.select('div.les-content > a')
            server_name = ' '.join(server.select_one('div.les-title').find_all(text=True, recursive=True)).encode(
                'utf8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for episode in episodes:
                movie['group'][server_name].append({
                    'link': episode.get('episode-id'),
                    'title': "%s" % episode.text.encode('utf8')
                })

        return movie

    def get_link(self, response, request, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        source = re.search(r'iframe.*id=(.*?)\\?"', response)
        if source:
            url = "{}/player/hls/getlink.php?id={}".format(domain, source.group(1))
            response = json.loads(request.get(url))
            Parser.create_link(movie['links'], response, domain)
            response = json.loads(request.get(url + '&type=hls'))
            Parser.create_link(movie['links'], response, domain)

        return movie

    @staticmethod
    def create_link(links, response, domain):
        if response.get('status') is 1:
            sources = json.loads(response.get('data'))
            for f in sources:
                url = f.get('file')
                if not 'http' in url:
                    url = 'https://{}'.format(url)
                links.append({
                    'link': url.replace('http://', 'https://').replace('////', '//'),
                    'title': 'Link %s' % f['label'],
                    'type': f['type'],
                    'resolve': False,
                    'originUrl': domain
                })
