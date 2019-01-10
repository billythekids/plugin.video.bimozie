# coding: utf8
from bs4 import BeautifulSoup
import urllib
import re
import json
from mozie_request import Request
from utils.link_parser import LinkParser


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("a.btn-see").get('href')

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
        ep_id = re.search("EpisodeID = '(.*)',", response).group(1)
        movie_id = re.search("MovieID = '(.*)';", response).group(1)

        servers = soup.select('div.list-server > div.server-item > div.option > span')
        episodes = soup.select('ul.list-episode > li')
        for server in servers:
            server_name = "%s - %s" % (server.text.strip().encode('utf-8'), movie_type.text.strip().encode('utf-8'))
            if server_name not in movie['group']: movie['group'][server_name] = []
            # if skipEps is False and len(episodes) > 0:
            for episode in episodes:
                movie['group'][server_name].append({
                    'link': '%s,%s,%s' % (movie_id, ep_id, server.get('data-index')),
                    'title': "Tap %s" % episode.select_one('a').text
                })

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        m = re.search("playerInstance.setup\({sources:\[(.*)\]", response)
        if m is not None:
            sources = '[%s]' % m.group(1)
            valid_json = re.sub(r'(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources)
            sources = json.loads(valid_json)
            if len(sources) > 1:
                sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
            if len(sources) > 0:
                source = sources[0]
                label = 'label' in source and source['label'] or ''
                movie['links'].append({
                    'link': source['file'],
                    'title': 'Link %s' % label.encode('utf-8'),
                    'type': label.encode('utf-8'),
                    'resolvable': True
                })

            return movie

        m = re.search('<iframe.*src=".*?url=(.*)" frameborder', response)
        if m is not None:
            source = urllib.unquote(m.group(1))
            movie['links'].append({
                'link': source,
                'title': '',
                'type': '',
                'resolvable': True
            })

            return movie

        # m = re.search('<iframe.*src="(.*)" frameborder', response)
        # if m is not None:
        #     source = urllib.unquote(m.group(1))
        #     print(source)
        #     LinkParser(source).get_link()
        #     # movie['links'].append({
        #     #     'link': source,
        #     #     'title': '',
        #     #     'type': '',
        #     #     'resolvable': True
        #     # })
        #
        #     return movie

        return movie
