# coding=utf-8
from bs4 import BeautifulSoup
import re
import json
from utils.mozie_request import Request


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('div.content > a.nutplay').get('href')

    def get(self, response, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.server-wrapper > div.server")
        if len(servers) > 0:
            for server in servers:
                server_name = server.select_one('label').getText().strip().encode('utf-8')
                if server_name not in movie['group']: movie['group'][server_name] = []
                for ep in server.select('ul.episodes > li > a'):
                    movie['group'][server_name].append({
                        'link': ep.get('href').encode('utf-8'),
                        'title': 'Episode %s' % ep.text.strip().encode('utf-8'),
                    })
        else:
            return self.get_link(response, originUrl)

        return movie

    def get_link(self, response, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.search('"sourceLinks": (\[.*\]),', response)
        if sources:
            sources = sources.group(1)
            for source in json.loads(sources):
                for link in source['links']:
                    movie['links'].append({
                        'link': link['file'].replace('\\', ''),
                        'title': 'Link %s' % link['label'].encode('utf-8'),
                        'type': link['label'].encode('utf-8'),
                        'resolve': False
                    })

            return movie

        sources = re.search("var urlPlay = '(.*)';", response)
        if sources:
            sources = sources.group(1)
            response = Request().get(sources)
            sources = re.search("var sources = (.*);", response)
            if sources:
                sources = json.loads(sources.group(1))
                if type(sources) is dict:
                    if 'file' in sources:
                        movie['links'].append({
                            'link': sources['file'].replace('\\', ''),
                            'title': 'Link %s' % sources['type'].encode('utf-8'),
                            'type': sources['type'].encode('utf-8'),
                            'originUrl': originUrl,
                            'resolve': False
                        })
                else:
                    for source in sources:
                            movie['links'].append({
                                'link': source['file'].replace('\\', ''),
                                'title': 'Link %s' % source['type'].encode('utf-8'),
                                'type': source['type'].encode('utf-8'),
                                'originUrl': originUrl,
                                'resolve': False
                            })

                return movie

        sources = re.search("<iframe.*src=\"(.*)\"", response)
        if sources:
            source = sources.group(1)
            title = 'movie3s.net' in source and 'Movie3s' or 'Unknow'
            movie['links'].append({
                'link': source,
                'title': 'Link %s' % title,
                'type': 'file',
                'originUrl': originUrl,
                'resolve': False
            })
            return movie

        return movie
