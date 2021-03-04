# -*- coding: utf-8 -*-
import re, json
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:

    def get(self, response, url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        soup = BeautifulSoup(response, "html.parser")

        # get episode if possible
        episodes = soup.select('ul.list-stream > li > a.btn')
        found = False
        if len(episodes) > 1:
            for episode in episodes:
                if 'javascript' in episode.get('href') or 'dangky' in episode.get('href'):
                    continue
                else:
                    found = True
                    movie['links'].append({
                        'link': episode.get('href'),
                        'title': py2_encode(episode.text.strip()),
                        'type': 'Unknown',
                        'originUrl': 'https://play.thuckhuya.com/',
                        'resolve': False
                    })

        if not found:
            movie['links'].append({
                'link': url,
                'title': 'Direct link',
                'type': 'Unknown',
                'resolve': False,
                'originUrl': 'https://play.thuckhuya.com/'
            })

        return movie
