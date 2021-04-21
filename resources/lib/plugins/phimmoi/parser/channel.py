#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
import utils.xbmc_helper as helper


class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('ul.pagination > li > a')
        helper.log("*********************** Get pages ")
        for item in pages:
            if item.text.strip() == py2_encode("Trang kế →"): channel['page'] = int(page)+1

        for movie in soup.select('ul.list-movie > li > a'):
            title = movie.select_one('span.movie-title-1').text.strip()
            type = ""
            if movie.select_one('span.ribbon') is not None:
                type = movie.select_one('span.ribbon').text.strip()
            if movie.select_one('span.movie-title-2') is not None:
                realtitle = movie.select_one('span.movie-title-2').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            thumb = re.search('url\((.*)\);', movie.select_one('div.movie-thumbnail').get('style')).group(1)

            channel['movies'].append({
                'id': py2_encode(movie.get('href')),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type),
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

            thumb = re.search(r"background-image:url\('(.*)'\)", movie.select_one('div.public-film-item-thumb').get('style')).group(1)

            channel['movies'].append({
                'id': py2_encode(movie.get('href')),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type),
            })

        return channel
