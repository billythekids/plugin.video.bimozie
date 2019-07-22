# coding=utf-8
from bs4 import BeautifulSoup
from utils.cpacker import cPacker as Packer
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('div.content > a.nutplay').get('href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.list_episodes > div.listserver")
        for server in servers:
            server_name = server.select_one('div.label').getText().strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('span.name > li > a'):
                movie['group'][server_name].append({
                    'link': ep.get('href').encode('utf-8'),
                    'title': 'Episode %s' % ep.text.strip().encode('utf-8'),
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.search(r'(eval\(function\(p,a,c,k,e,d\).*?)\s+?</script>', response)
        if sources:
            sources = sources.group(1)
            sources = Packer().unpack(sources)
            sources = re.search('sources:(.*?]),', sources)
            sources = re.sub(r'(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources.group(1))
            sources = json.loads(sources)
            score = {'sd': 1, 'hd': 2, '360p': 1, '480p': 2, '720p': 3, '1080p': 3}
            if len(sources) > 1:
                try:
                    sources = sorted(sources, key=lambda elem: elem['label'].lower() in score and score[
                        elem['label'].lower()] or 3, reverse=True)
                except:
                    pass
            for source in sources:
                movie['links'].append({
                    'link': source['file'].replace('\\', ''),
                    'title': 'Link %s' % source['type'].encode('utf-8'),
                    'type': source['type'].encode('utf-8'),
                    'resolve': False
                })

        sources = re.search(r'sources:\s?(\[.*?\]),', response)
        if sources:
            sources = sources.group(1)
            sources = json.loads(sources)
            try:
                sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
            except:
                pass
            for source in sources:
                movie['links'].append({
                    'link': source['file'].replace('\\', ''),
                    'title': 'Link %s' % source['label'].encode('utf-8'),
                    'type': source['type'].encode('utf-8'),
                    'resolve': False
                })

        sources = re.search(r'data-lazy-src="(.*?)"', response)
        if sources:
            source = sources.group(1)
            movie['links'].append({
                'link': source,
                'title': 'Link Unknow',
                'type': 'Unknow',
                'resolve': False
            })

        return movie
