# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re, time
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
        now = time.time()

        for movie in soup.select('div.list-channel > a.item'):
            thumb = None

            title = py2_encode(movie.select_one('div.title').text.strip())
            type = "Chưa diễn ra"
            realtitle = ""
            type = movie.select_one('div.time > span').get('data-time').strip()

            datetime_str = py2_encode(movie.select_one('div.time > span').get('data-time').strip())
            # datetime_str += " +0700"
            if datetime_str:
                datetime_object = time.strptime(datetime_str, '%Y-%m-%d %H:%M')  # 2019-10-26 20:30
                datetime_object = time.mktime(datetime_object)

                if now > datetime_object:
                    type = "[COLOR blue]Đang diễn ra[/COLOR] {}".format(type)

            label = "[{}] {}".format(type, title)
            channel['movies'].append({
                'id': movie.get('href'),
                'label': label,
                'title': title,
                'realtitle': realtitle,
                'thumb': thumb,
                'type': type
            })

        return channel
