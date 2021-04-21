# -*- coding: utf-8 -*-
import json
import re

from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from six.moves.urllib.parse import unquote
from utils.mozie_request import Request

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        # play_button = soup.find_all('a', class_=['btn-see', 'btn-danger'])[0]
        return soup.select_one("a.btn-see.btn-danger").get('href')

    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }
        soup = BeautifulSoup(response, "html.parser")

        movie_types = soup.select('div.control-box > div.episodes div.caption')
        episodes = soup.select('ul.list-episode')
        for i in range(len(movie_types)):
            items = episodes[i].select('li > a')
            self.get_server_link(items, movie_types[i], movie)

        return movie

    def get_server_link(self, episodes, movie_type, movie):
        for episode in episodes:
            server_name = "%s" % py2_encode(movie_type.select_one('span').text.strip())
            if server_name not in movie['group']: movie['group'][server_name] = []
            movie['group'][server_name].append({
                'link': episode.get('href'),
                'title': "%s" % py2_encode(episode.text)
            })

    def get_link(self, response, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        # get all movie links
        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select('div.list-server > div.server-item > div > span.btn')
        movie_id = re.search("MovieID\s?=\s?'(.*?)'", response).group(1)

        ep_id = soup.select_one('ul.list-episode > li > a.current')
        if ep_id:
            ep_id = ep_id.get('data-id')
        else:
            ep_id = re.search("EpisodeID\s?=\s?'(.*?)',", response).group(1)

        jobs = []
        links = []
        r = Request()
        for server in servers:
            sv_id = int(server.get('data-index'))
            url = "%s/ajax/player/" % domain
            params = {
                'id': movie_id,
                'ep': ep_id
            }
            if sv_id > 0: params['sv'] = sv_id
            Parser.extract_link(r.post(url, params=params), links)

        for link in links:
            movie['links'].append({
                'link': link[0],
                'title': 'Link %s' % link[1],
                'type': link[1],
                'resolve': False,
                'originUrl': domain
            })

        return movie

    @staticmethod
    def extract_link(response, movie_links):
        m = re.search(r"sources:\s?(\[.*?\])", response, re.DOTALL)
        if m is not None:
            sources = m.group(1)
            valid_json = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources)
            valid_json = valid_json.replace(',]', ']')
            sources = json.loads(valid_json)
            if len(sources) > 0:
                for s in sources:
                    source = Parser.parse_link(s['file'])
                    if source and source not in movie_links:
                        label = s.get('label') and s.get('label') or s.get('type')
                        movie_links.append((source, py2_encode(label)))

        m = re.search(r'<iframe.*?src=".*?url=(http.*)" frameborder', response)
        if m is not None:
            source = unquote(m.group(1))
            source = Parser.parse_link(source)
            if source and source not in movie_links:
                movie_links.append((source, ''))

        m = re.search(r'<iframe.*src="(http.*?)" frameborder', response)
        if m is not None:
            source = unquote(m.group(1)).replace('\\', '')
            source = Parser.parse_link(source)
            if source and source not in movie_links:
                movie_links.append((source, ''))

    @staticmethod
    def parse_link(url):
        r = re.search(r'getLinkSimple', url)
        if r:
            res = Request()
            res.get(url)
            url = res.get_request().url

        r = re.search(r'128.199.198.106/video\?url=(.*)', url)
        if r:
            url = unquote(r.group(1))
        if 'error' in py2_encode(url):
            return None

        r = re.search(r'^/iframe.*?ref=(.*)', url)
        if r:
            base_url = r.group(1)
            base_url = urlparse(base_url)
            base_url = base_url.scheme + '://' + base_url.netloc
            url = base_url + url

        return url
