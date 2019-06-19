# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.mozie_request import AsyncRequest
from utils.pastebin import PasteBin
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
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

        sources = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", response)
        if sources:
            res = Request()
            vkey = re.search('key=(.*)', sources.group(1)).group(1)
            # http://vl.animehay.tv/initPlayer/f555b31844becd2e378d4978457014521af38ab8e66834ade1062b44827ef642
            resp = res.post('http://vl.animehay.tv/initPlayer/%s' % vkey)
            resp = json.loads(resp)

            # if 'p2pdrive' in resp['availablePlayers']:
            #     data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('p2pdrive', vkey)))
            #     source = data['data']
            #
            #     if source:
            #         movie['links'].append({
            #             'link': source,
            #             'title': 'Link p2pdrive',
            #             'type': 'hls',
            #             'resolve': False
            #         })

            if 'fembed' in resp['availablePlayers']:
                data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('fembed', vkey)))
                data = res.get(data['data'])
                source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)
                if source:
                    movie['links'].append({
                        'link': source,
                        'title': 'Link fembed',
                        'type': 'mp4',
                        'resolve': False
                    })
                
            if 'okru' in resp['availablePlayers']:
                data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('okru', vkey)))
                data = res.get(data['data'])
                source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)
                if source:
                    movie['links'].append({
                        'link': source,
                        'title': 'Link okru',
                        'type': 'mp4',
                        'resolve': False
                    })

            if 'openload' in resp['availablePlayers']:
                data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('openload', vkey)))
                data = res.get(data['data'])
                source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)
                if source:
                    movie['links'].append({
                        'link': source,
                        'title': 'Link openload',
                        'type': 'mp4',
                        'resolve': False
                    })

            return movie

        sources = re.search('<script rel="nofollow" src="(.*)" async>', response)
        response = Request().get(sources.group(1))
        sources = json.loads(re.search('links: (.*?),', response).group(1))

        if len(sources) > 0:
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

        return movie
