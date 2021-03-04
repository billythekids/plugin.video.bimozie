# -*- coding: utf-8 -*-
import time

import utils.xbmc_helper as helper
from bs4 import BeautifulSoup


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

            title = helper.text_encode(movie.select_one('div.title').text.strip())
            type = "Chưa diễn ra"
            realtitle = ""
            type = movie.select_one('div.time > span').get('data-time').strip()

            datetime_str = helper.text_encode(movie.select_one('div.time > span').get('data-time').strip())
            # datetime_str += " +0700"
            if datetime_str:
                datetime_object = time.strptime(datetime_str, '%Y-%m-%d %H:%M')  # 2019-10-26 20:30
                datetime_object = time.mktime(datetime_object)

                if now > datetime_object:
                    type = "[COLOR blue]Đang diễn ra[/COLOR] {}".format(helper.text_encode(type))

            label = "[{}] {}".format(helper.text_encode(type), helper.text_encode(title))
            channel['movies'].append({
                'id': movie.get('href'),
                'label': helper.text_encode(label),
                'title': helper.text_encode(title),
                'realtitle': helper.text_encode(realtitle),
                'thumb': thumb,
                'type': helper.text_encode(type)
            })

        return channel
