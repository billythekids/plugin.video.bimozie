# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    @staticmethod
    def get(response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        current_time = int(round(time.time()))

        for movie in soup.select('div.matches__item'):
            if movie:
                ref = movie.select_one('a')
                title = ref.get('title')
                if not title:
                    continue

                murl = ref.get('href')
                if movie.get('data-runtime'):
                    start_time = int(movie.get('data-runtime'))
                else:
                    start_time = current_time + 1

                movie_type = ''
                if movie.select_one('div.matches__status--normal span.t_time'):
                    movie_type = movie.select_one('div.matches__status--normal span.t_time').get('data-time').strip()
                label = "{} - {}".format(movie_type, title)

                if current_time >= start_time:
                    status = "[COLOR blue]Đang diễn ra[/COLOR]"
                    label = "[{}] {} - {}".format(status, movie_type, title)

                channel['movies'].append({
                    'id': murl,
                    'label': py2_encode(label),
                    'title': py2_encode(title),
                    'realtitle': '',
                    'thumb': None,
                    'type': py2_encode(movie_type)
                })

        return channel
