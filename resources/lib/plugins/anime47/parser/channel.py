# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
import utils.xbmc_helper as helper


def text(txt):
    try:
        return txt.encode('latin1').decode('utf-8').strip()
    except:
        return py2_encode(txt, 'latin1').decode('utf-8').strip()

class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select_one('ul.pagination')

        helper.log("*********************** Get pages ")
        m = re.findall(r'(page)?[/|=](\d+)(.html)?', str(pages))
        if m:
            m = [int(x[1]) for x in m]
            channel['page'] = max(m)

        for movie in soup.select('ul#movie-last-movie > li a'):
            realtitle = ""
            title = movie.select_one('div.movie-title-1').text.strip()
            type = ""
            if movie.select_one('span.ribbon') is not None:
                type = movie.select_one('span.ribbon').text.strip()
            if movie.select_one('span.movie-title-2') is not None:
                realtitle = movie.select_one('span.movie-title-2').text.strip()

            if realtitle:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                realtitle = title
                label = "[%s] %s" % (type, title)

            thumb = re.search(r"background-image:url\('(.*)'\)",
                              movie.select_one('div.public-film-item-thumb').get('style')).group(1)

            channel['movies'].append({
                'id': text(movie.get('href')),
                'label': text(label),
                'title': text(title),
                'realtitle': text(realtitle),
                'thumb': thumb,
                'type': text(type)
            })

        return channel

    def getTop(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")

        for movie in soup.select('li > a.movie-item'):
            title = movie.select_one('div.movie-title-1').text.strip()
            realtitle = type = ""
            if movie.select_one('span.ribbon') is not None:
                type = movie.select_one('span.ribbon').text.strip()
            if movie.select_one('span.movie-title-2') is not None:
                realtitle = movie.select_one('span.movie-title-2').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            thumb = re.search(r"background-image:url\('(.*)'\)",
                              movie.select_one('div.public-film-item-thumb').get('style')).group(1)

            channel['movies'].append({
                'id': text(movie.get('href')),
                'label': text(label),
                'title': text(title),
                'realtitle': text(realtitle),
                'thumb': thumb,
                'type': text(type)
            })

        return channel
