# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request, AsyncRequest
from kodi_six.utils import py2_encode
import utils.xbmc_helper as helper
import re
import json
from utils.link_extractor import LinkExtractor


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
        #get server group
        for server_group in soup.select('div.movie-rate'):
            group_name = py2_encode(server_group.select_one('div.rate').text.strip())
            movie['group'][group_name] = []
            eps = server_group.select('div.movie-eps-wrapper > a.movie-eps-item')
            for i in range(len(eps)):
                ep = eps[i]
                if 'disabled' in ep.get('class'): continue
                movie['group'][group_name].append({
                    'link': py2_encode(ep.get('href')),
                    'title': py2_encode(ep.get('title')),
                })

        return movie

    def get_link2(self, response, originUrl, api):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        soup = BeautifulSoup(response, "html.parser")
        links = soup.select('div.video-footer a.btn-sv')

        jobs = []
        movie_links = []

        for link in links:
            url = link.get('data-href')
            jobs.append({'url': url, 'parser': Parser.parse_link, 'headers': {
                'referer': originUrl
            }})

        AsyncRequest().get(jobs, args=movie_links)
        for link in movie_links:
            movie['links'].append({
                'link': link,
                'title': 'Link hls',
                'type': 'hls',
                'resolve': False,
                'originUrl': originUrl
            })

        return movie

    @staticmethod
    def parse_link(response, movie_links):
        m_url = LinkExtractor.iframe(response)
        if m_url and 'dongphymtv.com' not in m_url:
            movie_links.append(m_url)

    # deprecated
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
        #     except Exception as e: helper.log(e)

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
