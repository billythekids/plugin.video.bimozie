# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
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
        last_page = soup.select('ul.page-numbers > li > a.page-numbers')
        helper.log("*********************** Get pages ")
        if len(last_page) > 1:
            channel['page'] = int(last_page[-2].text.strip())

        for movie in soup.select('a.halim-thumb'):
            title = movie.get('title').strip()
            realtitle = movie.select_one('h2.entry-title').text.strip()
            thumb = movie.select_one('img.img-responsive').get('src')
            type = movie.select_one('span.episode').text.strip()      
            label = "[%s] %s" % (type, title)
            intro = ""

            channel['movies'].append({
                'id': movie.get('href'),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type),
                'intro': py2_encode(intro),
            })

        return channel

    def getTop(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        for movie in soup.select('#halim-advanced-widget-3-ajax-box > article > div > a.halim-thumb'):
            # tag = movie.select_one('a')
            title = movie.get('title').strip()
            realtitle = type = ""
            if movie.select_one('span.episode') is not None:
                type = movie.select_one('span.episode').text.strip()           
            if movie.select_one('h2.entry-title') is not None:
                realtitle = movie.select_one('h2.entry-title').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)
            thumb = movie.select_one('img.img-responsive').get('src')           
            channel['movies'].append({
                'id': py2_encode(movie.get('href')),
                'label': py2_encode(label),
                'intro': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type),
            })
        return channel

    def search_result(self, response):
        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        try:
            soup = BeautifulSoup(response, "html.parser")

            for movie in soup.select('a.halim-thumb'):
                title = movie.get('title').strip()
                link = movie.get('href')
                thumb = movie.select_one('img.img-responsive').get('src')
                channel['movies'].append({
                    'id': movie.get('href'),
                    'label': title,
                    'title': title,
                    'realtitle': title,
                    'intro': title,
                    'thumb': thumb,
                    'type': ''
                })
        except: pass
        return channel
