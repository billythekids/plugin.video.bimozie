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

        for movie in soup.select('ul#movie-last-movie > li a'):
            real_title = ""
            title = ""
            movie_type = ""
            thumbnail = ""

            if real_title:
                label = "[%s] %s - %s" % (movie_type, title, real_title)
            else:
                real_title = title
                label = "[%s] %s" % (movie_type, title)

            channel['movies'].append({
                'id': text_encode(movie.get('href')),
                'label': text_encode(label),
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

        for movie in soup.select('li > a.movie-item'):
            real_title = ""
            title = ""
            movie_type = ""
            thumbnail = ""

            if real_title:
                label = "[%s] %s - %s" % (movie_type, title, real_title)
            else:
                real_title = title
                label = "[%s] %s" % (type, title)

            channel['movies'].append({
                'id': text_encode(movie.get('href')),
                'label': text_encode(label),
                'title': text_encode(title),
                'realtitle': text_encode(real_title),
                'thumb': thumbnail,
                'type': text_encode(type)
            })

        return channel
