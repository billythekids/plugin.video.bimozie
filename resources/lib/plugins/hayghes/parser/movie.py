# -*- coding: latin1 -*-
import re

from bs4 import BeautifulSoup
from utils.link_extractor import LinkExtractor
from utils.mozie_request import Request
from utils.xbmc_helper import text_encode
import utils.xbmc_helper as helper


class Parser:
    def get(self, response, referrer_url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get server group and link
        servers = soup.select('div.server')
        for server in servers:
            server_title = text_encode(server.select_one('h3.server-name').text.strip())
            if server_title not in movie['group']: movie['group'][server_title] = []
            self.get_server_eps(server, movie['group'][server_title])

        return movie

    @staticmethod
    def get_server_eps(content, group_link):
        for movie in content.select('ul > li > a'):
            group_link.append({
                'link': movie.get('href'),
                'title': "%s" % text_encode(movie.text)
            })

    def get_link(self, response, domain, referrer_url, request):
        helper.log("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # filmInfo.episodeID = parseInt('201326');
        # filmInfo.filmID = parseInt('15586');
        # filmInfo.playTech = 'auto';
        ep_id = re.search(r'''filmInfo.episodeID = parseInt\('(.*?)'\);''', response).group(1)
        film_id = re.search(r'''filmInfo.filmID = parseInt\('(.*?)'\);''', response).group(1)
        play_tech = re.search(r'''filmInfo.playTech = '(.*?)';''', response).group(1)
        response = Request().post('{}/ajax'.format(domain), params={
            'NextEpisode': 1,
            'EpisodeID': ep_id,
            'filmID': film_id,
            'playTech': play_tech
        })

        link = LinkExtractor.iframe(response)
        if link:
            movie['links'].append({
                'link': link,
                'title': 'Link HD',
                'type': 'stream',
                'resolve': False,
                'originUrl': referrer_url
            })

        # if links:
        #     for link in links:
        #         movie['links'].append({
        #             'link': link.get('file'),
        #             'title': 'Link %s' % link.get('label'),
        #             'type': link.get('label'),
        #             'resolve': False,
        #             'originUrl': referrer_url
        #         })

        return movie
