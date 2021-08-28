# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from utils.xbmc_helper import text_encode


class Parser:
    # Display movies in category list
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select_one('ul.pagination')
        m = re.findall(r'(page)?[/|=](\d+)(.html)?', str(pages))
        if m:
            m = [int(x[1]) for x in m]
            channel['page'] = max(m)

        for movie in soup.select('div.content > div.filmlist > div.item'):
            item = movie.select_one('a.poster')

            real_title = ""
            title = item.get('title')
            movie_type = movie.select_one('div.meta').find(text=True, recursive=False).strip()
            thumbnail = item.select_one('img').get('src')

            if real_title:
                label = "[%s] %s - %s" % (movie_type, title, real_title)
            else:
                real_title = title
                label = "[%s] %s" % (movie_type, title)

            intro = label
            if movie.select_one('div.meta'):
                intro = '[{}] {} - {}'.format(movie.select_one('div.icons > div.quality').text,
                                              movie.select_one('div.meta').text, title)

            channel['movies'].append({
                'id': text_encode(item.get('href')),
                'label': text_encode(label),
                'intro': text_encode(intro),
                'title': text_encode(title),
                'realtitle': text_encode(real_title),
                'thumb': thumbnail,
                'type': text_encode(movie_type)
            })

        return channel

    # Display news/host movie on category list
    def getTop(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")

        for movie in soup.select('div#slider > div.swiper-wrapper > div.item'):
            real_title = ""
            title = movie.select_one('h3.title').text
            movie_type = movie.select_one('div.meta > span.quality').text
            thumbnail = movie.get('data-src')

            intro = title
            if movie.select_one('div.desc'):
                intro = movie.select_one('div.desc').text

            if real_title:
                label = "[%s] %s - %s" % (movie_type, title, real_title)
            else:
                real_title = title
                label = "[%s] %s" % (movie_type, title)

            channel['movies'].append({
                'id': text_encode(movie.get('href')),
                'label': text_encode(label),
                'intro': intro,
                'title': text_encode(title),
                'realtitle': text_encode(real_title),
                'thumb': thumbnail,
                'type': text_encode(movie_type)
            })

        return channel
