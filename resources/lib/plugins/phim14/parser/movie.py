# coding: utf8
import re
import json
import urllib
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.link_parser import LinkParser


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
            server_name = server.select_one('strong').find(text=True, recursive=False).strip().encode('utf-8')
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
                'link': source,
                'title': '',
                'type': '',
                'resolvable': True
            })
            return movie

        sources = re.search('<iframe.*src=(".*?")', response)
        if sources is not None:
            source = LinkParser(sources.group(1).replace('"', '')).get_link()
            if source:
                movie['links'].append({
                    'link': source[0],
                    'title': 'Link %s' % source[1].encode('utf-8'),
                    'type': source[1].encode('utf-8'),
                    'resolvable': False
                })
                return movie

        sources = re.search('"sources": (.*),', response)
        if sources is not None:
            sources = json.loads(sources.group(1))
            if 'error' not in sources:
                if len(sources) > 1:
                    sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
                if len(sources) > 0:
                    source = sources[0]
                    label = 'label' in source and source['label'] or ''
                    movie['links'].append({
                        'link': source['file'].replace('\\', ''),
                        'title': 'Link %s' % label.encode('utf-8'),
                        'type': label.encode('utf-8'),
                        'resolvable': True
                    })
                    return movie

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
