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

        # get all server list
        mid = None
        try:
            mid = re.search(r'drt:direction,mid:"(.*)",idx:idx,', response).group(1)
        except: pass
        if not mid:
            mid = re.search(r'mid:\s?"(.*?)",', response).group(1)


        list_eps = re.search(r'div class="movie-eps-nav" data-min="(\d+)" data-max="(\d+)"', response)
        # http://dongphim.net/content/subitems?drt=down&mid=8ghRyAh1&idx=400
        request = Request()
        idx = int(list_eps.group(1))
        eps = ""
        while True:
            if idx < 11:
                break
            else:
                url = "http://dongphim.net/content/subitems?drt=down&mid=%s&idx=%s" % (mid, idx)
                data = json.loads(request.get(url))
                eps += data['data']
                idx = data['idx']

        eps = eps.replace('\t\n\t', '')
        eps = eps.replace('\n\t\t', '')
        eps = eps.replace('\\\"', '"')
        eps = eps.replace('\n\t', '')
        eps = eps.replace('\t', '')

        soup = BeautifulSoup(eps, "html.parser")
        movie['group']['Dongphim'] = []
        eps = soup.select('a.movie-eps-item')
        for i in reversed(range(len(eps))):
            ep = eps[i]
            if 'disabled' in ep.get('class'): continue
            movie['group']['Dongphim'].append({
                'link': ep.get('href').encode('utf-8'),
                'title': ep.get('title').encode('utf-8'),
            })

        soup = BeautifulSoup(response, "html.parser")
        eps = soup.select('a.movie-eps-item')
        for i in reversed(range(len(eps))):
            ep = eps[i]
            if 'disabled' in ep.get('class'): continue
            movie['group']['Dongphim'].append({
                'link': ep.get('href').encode('utf-8'),
                'title': ep.get('title').encode('utf-8'),
            })

        return movie

    def get_link(self, response):
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
                'url': source['url'],
                'bk_url': source['burl'],
                'pr_url': source['purl'],
                'ex_hls[]': source['exhls'],
                'prefer': prefers[0],
                'ts': 1556547428839,
                'item_id': item_id,
                'username': username,
            }

            response = Request().get('http://dongphim.net/content/parseUrl', params=params)
            response = json.loads(response)

            if not response['hls']:
                self.get_media_url(response, movie['links'])

            params_alt = {
                'v': 2,
                'url': source['url'],
                'bk_url': source['burl'],
                'pr_url': source['purl'],
                'ex_hls[]': source['exhls'],
                'prefer': prefers[0],
                'ts': 1556547428839,
                'item_id': item_id,
                'username': username,
                'err[pr][ended]': 'true',
                'err[eh][num]': 1,
                'err[eh][dr][]': 'https://ok.ru',
            }

            response = json.loads(Request().get('http://dongphim.net/content/parseUrl', params=params_alt))
            self.get_media_url(response, movie['links'])

        if len(movie['links']) > 1:
            try:
                movie['links'] = sorted(movie['links'], key=lambda elem: int(re.search(r'(\d+)', elem['title']).group(1)), reverse=True)
            except Exception as e: print(e)

        return movie

    def get_media_url(self, response, movie):
        urls = response['formats']

        for i in urls:
            movie.append({
                'link': urls[i],
                'title': 'Link %s' % i,
                'type': 'mp4',
                'resolve': False,
            })
