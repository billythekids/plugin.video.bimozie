# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response, page):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        tab = soup.find('div', {'class': 'tab-pane', 'id': page})

        movies = tab.select('a')
        for movie in movies:
            channel['movies'].append({
                'id': movie.get('href'),
                'label': py2_encode(movie.get('title')),
                'title': py2_encode(movie.get('data-key')),
                'realtitle': py2_encode(movie.get('data-key')),
                'thumb': movie.select_one('img').get('src'),
                'type': ''
            })

        return channel
