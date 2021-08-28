# -*- coding: utf-8 -*-
import re, json
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:

    def get(self, response, url, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        soup = BeautifulSoup(response, "html.parser")

        # get episode if possible
        episodes = soup.select('ul.live-nav-links > li.item')
        found = False
        if len(episodes) > 1:
            for episode in episodes:
                print(episode)
                if episode.get('data-url'):
                    found = True
                    movie['links'].append({
                        'link': "%s" % (episode.get('data-url')),
                        'title': py2_encode(episode.select_one('a').text.strip()),
                        'type': 'Unknown',
                        'originUrl': url,
                        'resolve': False
                    })

        if not found:
            movie['links'].append({
                'link': url,
                'title': 'Direct link',
                'type': 'Unknown',
                'resolve': False,
                'originUrl': url
            })

        return movie
