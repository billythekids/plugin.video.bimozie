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

        for item in soup.select('div#ajax-content-lives > div.list-channel'):
            movie = item.select_one('a div.info')
            if movie:
                murl = item.select_one('a').get('href')
                start_time = int(item.get('data-runtime'))
                title = movie.select_one('div.title').text.strip()
                movie_type = movie.select_one('div.t_time').text.strip()
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
