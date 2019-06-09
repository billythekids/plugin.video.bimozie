# -*- coding: utf-8 -*-
import re
import json
import urllib
from bs4 import BeautifulSoup
from utils.mozie_request import Request


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
        servers = soup.select("div.serverlist > div.server")
        for server in servers:
            server_name = server.select_one('div.label').find(text=True, recursive=False).strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.episodelist li a'):
                movie['group'][server_name].append({
                    'link': ep.get('href'),
                    'title': 'Tập %s' % ep.text.encode('utf-8'),
                })

        return movie

    def get_link(self, response, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        sources = re.search('gkpluginsphp\("mediaplayer", {link: "(.*)"}\);', response)

        if sources is not None:
            get_link_response = Request().post('http://www.kenh88.com/gkphp/plugins/gkpluginsphp.php',
                                               {'link': sources.group(1)})
            source = json.loads(get_link_response)
            movie['links'].append({
                'link': source['link'],
                'title': 'Link',
                'type': '',
                'originUrl': originUrl,
                'resolve': False
            })
            return movie

        sources = re.search('var sources = (.*)', response)
        if sources is not None:
            sources = self.remove_duplicate(json.loads(sources.group(1)))
            sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
            for source in sources:
                movie['links'].append({
                    'link': source['file'],
                    'title': 'Link %s' % source['label'].encode('utf-8'),
                    'type': source['label'].encode('utf-8'),
                    'originUrl': originUrl,
                    'resolve': False
                })
            return movie

        sources = re.search('<iframe.*src=(".*?")', response)
        if sources is not None:
            source = sources.group(1).replace('"', '')
            if source:
                movie['links'].append({
                    'link': source,
                    'title': 'Link %s' % source.encode('utf-8'),
                    'type': 'Unknow',
                    'originUrl': originUrl,
                    'resolve': False
                })
                return movie

        sources = re.search('sources: ({.*}),', response)
        if sources is not None:
            source = sources.group(1).replace('\\', '')
            source = json.loads(source)
            if source:
                movie['links'].append({
                    'link': source['file'],
                    'title': 'Link %s' % 'Auto',
                    'type': 'Auto',
                    'originUrl': originUrl,
                    'resolve': False
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
