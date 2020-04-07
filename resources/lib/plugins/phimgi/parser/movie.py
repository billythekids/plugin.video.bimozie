# coding=utf-8
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest, Request
import utils.xbmc_helper as helper
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        return re.search('post_id: (\d+),', response).group(1), \
               re.search('var ajax_player.*"nonce":"(.*)"};', response).group(1)

    def get(self, response, nonce):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")

        # get all server list
        servers = soup.select("div.halim-server")
        for server in servers:
            server_name = server.select_one('span.halim-server-name').getText().strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.halim-list-eps > li > span'):
                # postid|serverid|epid|nounce
                id = "%s|%s|%s|%s" % (ep.get('data-post-id'), ep.get('data-server'), ep.get('data-episode'), nonce)
                movie['group'][server_name].append({
                    'link': id,
                    'title': ep.text.strip().encode('utf-8'),
                })

        return movie

    def get_link(self, data, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # get all server list
        # data = postid|serverid|epid|nounce
        params = {
            'action': 'halim_get_listsv',
            'episode': data[2],
            'server': data[1],
            'postid': data[0],
            'nonce': data[3],
        }

        jobs = []
        url = "%s/wp-admin/admin-ajax.php" % domain
        response = Request().post(url, params)

        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select("span")
        for server in servers:
            params = {
                # 'action': 'halim_ajax_player',
                'action': 'halim_play_listsv',
                'episode': data[2],
                'server': data[1],
                'postid': data[0],
                'nonce': data[3],
                'ep_link': server.get('data-url')
            }
            jobs.append({'url': url, 'params': params, 'parser': Parser.extract_link})
        AsyncRequest().post(jobs, args=movie['links'])

        return movie

    @staticmethod
    def extract_link(response, movie_links):
        sources = re.search('<iframe.*src=(".*?")', response)
        if sources is not None:
            source = sources.group(1).replace('"', '')
            if source:
                movie_links.append({
                    'link': source,
                    'title': 'Link %s' % source.encode('utf-8'),
                    'type': 'Unknow',
                    'resolve': False,
                    'originUrl': source

                })

    def parse_link(self, url):
        return url
