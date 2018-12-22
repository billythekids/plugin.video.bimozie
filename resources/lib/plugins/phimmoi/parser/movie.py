# coding: utf8
from bs4 import BeautifulSoup
import re
import base64


class Parser:
    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")

        # get episode if possible
        episodes = soup.select('ul.list-episode li a')
        if skipEps is False and len(episodes) > 0:
            for episode in episodes:
                movie['episode'].append({
                    'link': episode.get('href'),
                    'title': episode.get('title').encode('utf-8'),
                })

        else:
            print("***********************Get Movie Link*****************************")

        return movie


