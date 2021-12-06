# -*- coding: utf-8 -*-
import json
import re

import utils.xbmc_helper as helper
from bs4 import BeautifulSoup
from utils.xbmc_helper import text_encode


class Parser:
    @staticmethod
    def get_play_link(response):
        soup = BeautifulSoup(response, "html.parser")
        # get server group and link
        play_button = str(soup.select_one('div.btn-group button:first-child'))
        # onclick="location.href='https://www.hhkungfu.tv/p/mo-vuong-chi-vuong-phan-4-video.html'
        return re.search(r"location.href='(.*?)'", play_button).group(1)

    @staticmethod
    def get(response, referrer_url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        links = re.findall(r'''var\slink(\d)_(\d+)\s=\s"(.*?)"''', response)
        server_name = 'hhkungfu.tv'
        movie['group'][server_name] = []
        movie_links = {}

        for link in links:
            (ep, chapter, movie_link) = link
            if chapter not in movie_links:
                movie_links[chapter] = []
            movie_links[chapter].append(movie_link)

        for chapter in movie_links:
            movie['group'][server_name].append({
                'link': json.dumps(movie_links[chapter]),
                'title': "%s" % text_encode(chapter),
                'originUrl': referrer_url
            })

        return movie

    def get_link(self, response, domain, referrer_url, request):
        helper.log("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        links = json.loads(response)
        for link in links:
            # get server list
            movie['links'].append({
                'link': link,
                'title': 'Link',
                'type': 'hls',
                'resolve': False,
                'originUrl': referrer_url
            })

        return movie
