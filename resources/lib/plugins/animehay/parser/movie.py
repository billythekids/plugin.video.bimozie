# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
import re
import json
import urllib


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    key = "PhimMoi.Net@"

    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('div#ah-pif > div.ah-pif-head > div.ah-pif-ftool > div.ah-float-left > span > a').get(
            'href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.ah-wf-body > div.ah-wf-le")
        for server in servers:
            server_name = server.select_one('div.ah-le-server > span').text.strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul > li > a'):
                movie['group'][server_name].append({
                    'link': ep.get('href').encode('utf-8'),
                    'title': 'Episode %s' % ep.text.encode('utf-8'),
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        try:
            sources = re.search('<script rel="nofollow" src="(.*)" async>', response)
            response = Request().get(sources.group(1))
            sources = json.loads(re.search('links: (.*),', response).group(1))

            for key, value in sources.items():
                if value:
                    label = key[1:].encode('utf-8')
                    movie['links'].append({
                        'link': value,
                        'title': 'Link %s' % label,
                        'type': label,
                        'resolve': True
                    })

            movie['links'] = sorted(movie['links'], key=lambda elem: int(elem['type']), reverse=True)
            print(movie)
        except:
            pass

        return movie
