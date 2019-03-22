# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
import json
from utils.mozie_request import Request


class Parser:
    def get(self, response, skipEps=False):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }
        soup = BeautifulSoup(response, "html.parser")

        movie_types = soup.select('ul.choose-server > li > a')
        for movie_type in movie_types:
            if re.search('http', movie_type.get('href')):
                response = Request().get(movie_type.get('href'))
                soup = BeautifulSoup(response, "html.parser")
                self.get_server_link(soup, response, movie_type, movie)
            else:
                self.get_server_link(soup, response, movie_type, movie)

        return movie

    def get_server_link(self, soup, response, movie_type, movie):
        movie_id = re.search("MovieID = '(.*)';", response).group(1)

        servers = soup.select('div.list-server > div.server-item > div.option > span')
        episodes = soup.select('ul.list-episode > li > a')
        for server in servers:
            server_name = "%s - %s" % (server.text.strip().encode('utf-8'), movie_type.text.strip().encode('utf-8'))
            if server_name not in movie['group']: movie['group'][server_name] = []
            # if skipEps is False and len(episodes) > 0:
            for episode in episodes:
                ep_id = episode.get('data-id')
                movie['group'][server_name].append({
                    'link': '%s,%s,%s' % (movie_id, ep_id, server.get('data-index')),
                    'title': "Tap %s" % episode.text.encode('utf-8')
                })

    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("a.btn-see").get('href')

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        m = re.search("sources:\s?(\[.*?\])", response)
        if m is not None:
            sources = m.group(1)
            valid_json = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources)
            valid_json = valid_json.replace(',]', ']')
            sources = json.loads(valid_json)
            if len(sources) > 1:
                try:
                    sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
                except:
                    pass

            if len(sources) > 0:
                source = sources[0]
                label = 'label' in source and source['label'] or ''
                movie['links'].append({
                    'link': self.parse_link(source['file']),
                    'title': 'Link %s' % label.encode('utf-8'),
                    'type': label.encode('utf-8'),
                    'resolve': False
                })

            return movie

        m = re.search('<iframe.*src=".*?url=(.*)" frameborder', response)
        if m is not None:
            source = urllib.unquote(m.group(1))
            movie['links'].append({
                'link': self.parse_link(source),
                'title': '',
                'type': '',
                'resolve': True
            })

            return movie

        m = re.search('<iframe.*src="(.*)" frameborder', response)
        if m is not None:
            source = urllib.unquote(m.group(1)).replace('\\', '')
            if source:
                movie['links'].append({
                    'link': self.parse_link(source),
                    'title': source,
                    'type': 'Unknow',
                    'resolve': False
                })
                return movie

        return movie

    def parse_link(self, url):
        r = re.search('getLinkSimple', url)
        if r:
            res = Request()
            res.get(url)
            url = res.get_request().url

        r = re.search('128.199.198.106/video\?url=(.*)', url)
        if r:
            url = urllib.unquote(r.group(1))

        return url
