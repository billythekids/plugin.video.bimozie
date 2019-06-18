# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
import json
from utils.mozie_request import Request
from utils.mozie_request import AsyncRequest


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("a.btn-see").get('href')

    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }
        soup = BeautifulSoup(response, "html.parser")

        movie_types = soup.select('ul.choose-server > li > a')
        for movie_type in movie_types:
            if re.search('http', movie_type.get('href')):
                response = Request().get(movie_type.get('href'))
                soup = BeautifulSoup(response, "html.parser")
                self.get_server_link(soup, movie_type, movie)
            else:
                self.get_server_link(soup, movie_type, movie)

        return movie

    def get_server_link(self, soup, movie_type, movie):
        episodes = soup.select('ul.list-episode > li > a')
        for episode in episodes:
            server_name = "%s" % (movie_type.text.strip().encode('utf-8'))
            if server_name not in movie['group']: movie['group'][server_name] = []
            movie['group'][server_name].append({
                'link': episode.get('href'),
                'title': "Tập %s" % episode.text.encode('utf-8')
            })

    def get_link(self, response, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        # get all movie links
        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select('div.list-server > div.server-item > div.option > span')
        movie_id = re.search("MovieID\s?=\s?'(.*?)';", response).group(1)
        ep_id = soup.select_one('ul.list-episode > li > a.current').get('data-id')

        jobs = []
        links = []
        for server in servers:
            sv_id = server.get('data-index')
            url = "%s/ajax/player/" % domain
            params = {
                'id': movie_id,
                'ep': ep_id,
                'sv': sv_id
            }
            jobs.append({'url': url, 'params': params, 'parser': Parser.extract_link})

        AsyncRequest().post(jobs, args=links)
        for link in links:
            movie['links'].append({
                'link': link[0],
                'title': 'Link %s' % link[1],
                'type': link[1],
                'resolve': False
            })

        return movie

    @staticmethod
    def extract_link(response, movie_links):
        m = re.search(r"sources:\s?(\[.*?\])", response)

        if m is not None:
            sources = m.group(1)
            valid_json = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources)
            valid_json = valid_json.replace(',]', ']')
            sources = json.loads(valid_json)
            if len(sources) > 1:
                try:
                    sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
                except:
                    pass

            if len(sources) > 0:
                for s in sources:
                    source = Parser.parse_link(s['file'])
                    if source and source not in movie_links:
                        movie_links.append((source, s['label'].encode('utf-8')))

        m = re.search('<iframe.*src=".*?url=(.*)" frameborder', response)
        if m is not None:
            source = urllib.unquote(m.group(1))
            source = Parser.parse_link(source)
            if source and source not in movie_links:
                movie_links.append((source, ''))

        m = re.search('<iframe.*src="(.*)" frameborder', response)
        if m is not None:
            source = urllib.unquote(m.group(1)).replace('\\', '')
            source = Parser.parse_link(source)
            if source and source not in movie_links:
                movie_links.append((source, ''))

    @staticmethod
    def parse_link(url):
        r = re.search('getLinkSimple', url)
        if r:
            res = Request()
            res.get(url)
            url = res.get_request().url

        r = re.search('128.199.198.106/video\?url=(.*)', url)
        if r:
            url = urllib.unquote(r.group(1))
        if 'error' in url.encode('utf-8'):
            return None

        return url
