# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('div.tt-details a.watch').get('href')

    def get(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        url = re.search(r'"srcUrl"\s?:\s?"(.*?)",', response).group(1)
        url = 'https://%s/s.mp4' % url

        # subtitle
        subtitle = []
        soup = BeautifulSoup(response, "html.parser")
        tracks = soup.select('video > track')
        if tracks:
            for track in tracks:
                subtitle.append(track.get('src'))
            subtitle.reverse()

        server_name = 'Xemphim'
        movie['group'][server_name] = []

        movie['group'][server_name].append({
            'link': url,
            'title': 'Link direct',
            'type': 'mp4',
            'subtitle': subtitle,
            'resolve': True
        })

        return movie

    def get_link(self, video):

        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        movie['links'].append(video)
        return movie
