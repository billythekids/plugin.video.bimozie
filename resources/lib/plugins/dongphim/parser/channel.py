# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
import utils.xbmc_helper as helper
import re


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
        m = re.findall(r'-(\d+)', str(pages))
        if m:
            m = [int(x) for x in m]
            channel['page'] = max(m)

        for movie in soup.select('div.flex-wrap-movielist > a.movie-item'):

            title = movie.select_one('div.pl-carousel-content h6').text.strip()
            realtitle = movie.select_one('div.pl-carousel-content p').text.strip()
            type = movie.select_one('div.badget-eps')
            if type:
                type = type.text.strip()
            elif movie.select_one('div.pl-carousel-badget'):
                type = movie.select_one('div.pl-carousel-badget').text.strip()
            else:
                type = "HD"

            label = "[%s] %s - %s" % (type, title, realtitle)
            thumb = movie.select_one('div.img').get('data-original')

            channel['movies'].append({
                'id': movie.get('href'),
                'label': py2_encode(label),
                'intro': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type),
                # 'intro': movie.select_one('div.des > small').text.strip().encode("utf-8"),
            })

        return channel

    def getTop(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        for movie in soup.select('div.pl-carousel-cell > a'):

            title = movie.select_one('div.pl-carousel-content h6').text.strip()
            realtitle = movie.select_one('div.pl-carousel-content p').text.strip()
            type = movie.select_one('div.badget-eps')
            if type:
                type = type.text.strip()
            elif movie.select_one('div.pl-carousel-badget'):
                type = movie.select_one('div.pl-carousel-badget').text.strip()
            else:
                type = "HD"

            label = "[%s] %s - %s" % (type, title, realtitle)
            thumb = movie.select_one('div.img').get('data-original')

            channel['movies'].append({
                'id': movie.get('href'),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type),
                # 'intro': movie.select_one('div.des > small').text.strip().encode("utf-8"),
            })

        return channel
