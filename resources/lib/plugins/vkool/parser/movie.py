# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
import json
from utils.mozie_request import Request
from utils.mozie_request import AsyncRequest
from utils.aes import CryptoAES
from hashlib import md5


class Parser:

    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }
        soup = BeautifulSoup(response, "html.parser")

        servers = soup.select('div#list_episodes > div.listserver > div.name')
        server_episodes = soup.select('div#list_episodes > div.listserver > div.list_ep')

        i = 0
        for server_episode in server_episodes:
            server_name = servers[i].text.strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []

            for episode in server_episode.select('a'):
                movie['group'][server_name].append({
                    'link': episode.get('href'),
                    'title': "Tập %s" % episode.text.encode('utf-8')
                })
            i += 1
        return movie

    def get_link(self, response, domain, originUrl, request):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        # get all movie links
        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select('ul.list-episode > li.episode > a.episode-link')

        # find subtitle
        subtitle = None
        match_sub = re.search(r'window.subback\s?=\s?"(.*?)";', response)
        if match_sub:
            subtitle = match_sub.group(1)

        jobs = []
        links = []
        for server in servers:
            ep_id = server.get('data-ep')
            url = "%s/index.php" % domain
            params = {
                'ep': ep_id
            }
            jobs.append({'url': url, 'params': params, 'parser': Parser.extract_link})

        AsyncRequest(request=request).post(jobs, args=links)
        jobs = []
        movie_links = []

        for link in links:
            url = "%s/js/vkphp/plugins/gkpluginsphp.php" % domain
            jobs.append({'url': url, 'params': {
                'link': link
            }, 'parser': Parser.parse_link, 'responseHeader': True})

        AsyncRequest(request=request).post(jobs, args=movie_links)

        for link in movie_links:
            movie['links'].append({
                'link': link[0],
                'title': 'Link %s' % link[1],
                'type': link[1],
                'resolve': False,
                'subtitle': subtitle,
                'originUrl': originUrl
            })

        return movie

    @staticmethod
    def extract_link(response, movie_links):
        m = re.search(r'window.onerr\s?=\s\\"(.*?)\\";', response)

        if m is not None:
            source = m.group(1)
            if ('==|' in source):
                movie_links.append(source)

        m = re.search(r'curplay:\\"(.*?)\\",', response)
        if m is not None:
            source = m.group(1)
            movie_links.append(source)

    @staticmethod
    def parse_link(response, movie_links, response_headers):
        sources = json.loads(response)
        if 'link' in sources:
            if isinstance(sources['link'], list):
                for source in sources['link']:
                    if 'http' in source['link']:
                        movie_links.append((source['link'], source['label']))
                    else:
                        key = md5(response_headers.get('Expires')).hexdigest()
                        source['link'] = CryptoAES().decrypt(source['link'], key)
                        movie_links.append((source['link'], source['label']))
            elif 'http' in sources['link']:
                movie_links.append((sources['link'], 'label' in sources and sources['label'] or '720p'))

        return movie_links
