# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
import re
import json


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
        movie['group']['Dongphim'] = []
        eps = soup.select('div.movie-eps-wrapper > a.movie-eps-item')
        for i in reversed(range(len(eps))):
            ep = eps[i]
            if 'disabled' in ep.get('class'): continue
            movie['group']['Dongphim'].append({
                'link': ep.get('href').encode('utf-8'),
                'title': ep.get('title').encode('utf-8'),
            })

        return movie

    def get_link(self, response, originUrl, api):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.search(r"this.urls\s?=\s?(\[.*?\]);", response)
        username = re.search(r'username\s?:\s?[\'|"](\w+)[\'|"]', response).group(1)
        item_id = re.search(r'item_id\s?:\s?[\'|"](\w+)[\'|"]', response).group(1)
        prefers = json.loads(re.search(r'this.checkBestProxy\(\s?(\[.*?\])', response).group(1))

        if sources:
            source = json.loads(sources.group(1))[0]
            params = {
                'v': 2,
                'url': "",
                'bk_url': source['burl'],
                'pr_url': source['purl'],
                'if_url[]': source.get('iurl'),
                'vd_url[]': source.get('vdurl'),
                'prefer': prefers[0],
                'ts': 1556547428839,
                'item_id': item_id,
                'username': username,
            }

            response = Request().get('{}/content/parseUrl'.format(api), params=params)
            response = json.loads(response)

            if response.get('formats'):
                self.get_media_url(response, movie['links'], originUrl)

            params_alt = {
                'v': 2,
                'len': 1,
                'url': "",
                'bk_url': source['burl'],
                'pr_url': source['purl'],
                'if_url[]': source.get('iurl'),
                'vd_url[]': source.get('vdurl'),
                'rts_url[]': source.get('rtsurl'),
                'prefer': prefers[0],
                'ts': 1556547428839,
                'item_id': item_id,
                'username': username,
                'err[{}][dr][]'.format(response.get('type')): 'https://r1---sn-a5mekned.c.youtube.com',
                'err[{}][num]'.format(response.get('type')): 1,
                'err[{}][dr_s]'.format(response.get('type')): response.get('sig'),
                # 'err[pr][ended]': 'true',
                # 'err[do][ended]': 'true',
                # 'err[hdx][ended]': 'true',
                # 'err[eh][num]': 1,
                # 'err[eh][dr][]': 'https://ok.ru',
                # 'err[gbak][dr][]': 'https://sgp.dgo.dongphim.net'
            }

            response = json.loads(Request().get('{}/content/parseUrl'.format(api), params=params_alt))
            Parser.get_media_url(response, movie['links'], originUrl)

        # if len(movie['links']) > 1:
        #     try:
        #         movie['links'] = sorted(movie['links'], key=lambda elem: int(re.search(r'(\d+)', elem['title']).group(1)), reverse=True)
        #     except Exception as e: print(e)

        return movie

    @staticmethod
    def get_media_url(response, movie, originUrl):
        urls = response['formats']

        for i in urls:
            movie.append({
                'link': urls[i],
                'title': 'Link %s' % i,
                'type': 'mp4',
                'resolve': False,
                'originUrl': originUrl
            })
