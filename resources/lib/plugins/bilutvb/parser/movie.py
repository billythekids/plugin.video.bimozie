# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
import json
from utils.mozie_request import Request


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("a.watch-movie").get('href')

    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }
        soup = BeautifulSoup(response, "html.parser")

        servers = soup.select('div#halim-list-server > div.halim-server')
        for server in servers:
            episodes = server.select('ul.halim-list-eps > li > a')
            server_name = server.select_one('span.halim-server-name').find(text=True, recursive=False).encode('utf8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for episode in episodes:
                movie['group'][server_name].append({
                    'link': episode.get('href'),
                    'title': "Tập %s" % episode.text.encode('utf8')
                })

        return movie

    def get_link(self, response, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        # get all movie links
        nonce = re.search(r'ajax_player\s?=.*"nonce":"(.*?)"', response).group(1)
        post_id = re.search(r'"post_id":"(\d+)",', response).group(1)
        episode = re.search(r'episode:\s?(\d+),', response).group(1)
        server = re.search(r'server:\s?(\d+),', response).group(1)
        response = Request().post("https://bilutvb.com/wp-admin/admin-ajax.php", params={
            "action": "halim_ajax_player",
            "nonce": nonce,
            "episode": episode,
            "server": server,
            "postid": post_id
        })

        movie_links = []

        m = re.search(r"sources:\s?(\[.*?\])", response)

        if m is not None:
            sources = m.group(1)
            valid_json = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources)
            valid_json = valid_json.replace(',]', ']')
            sources = json.loads(valid_json)
            if len(sources) > 0:
                for s in sources:
                    movie_links.append((s['file'], s.get('label')))

        for link in movie_links:
            movie['links'].append({
                'link': link[0],
                'title': 'Link %s' % link[1],
                'type': link[1],
                'resolve': False,
                'originUrl': domain
            })

        return movie
