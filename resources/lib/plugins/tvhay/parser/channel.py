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
        last_page = soup.select_one('div.wp-pagenavi > a.last')
        helper.log("*********************** Get pages ")
        if last_page is not None:
            page = re.search('/(\d+)/$', last_page.get('href')).group(1)
            channel['page'] = int(page)

        movies = soup.select('ul.list-film > li > div.inner')
        if len(movies) > 0:
            for movie in movies:
                title = movie.select_one('div.name > a').find(text=True, recursive=False).strip()
                type = ""
                realtitle = ""

                if movie.select_one('div.status') is not None:
                    type = movie.select_one('div.status').text.strip()
                if movie.select_one('div.name2') is not None:
                    realtitle = movie.select_one('div.name2').text.strip()
                if realtitle is not None:
                    label = "[%s] %s - %s" % (type, title, realtitle)
                else:
                    label = "[%s] %s" % (type, title)

                thumb = movie.select_one('a img.lazy').get('data-original')

                channel['movies'].append({
                    'id': movie.select_one('div.name > a').get('href'),
                    'label': py2_encode(label),
                    'title': py2_encode(title),
                    'realtitle': py2_encode(realtitle),
                    'thumb': thumb,
                    'type': py2_encode(type),
                })

        movies = soup.select('div.totalService > article.post')
        if len(movies) > 0:
            for movie in movies:
                title = movie.select_one('div.descService > h2 > a').find(text=True, recursive=False).strip()
                type = ""
                realtitle = ""
                label = title
                intro = movie.select_one('div.descService > p').find(text=True, recursive=False).strip()
                thumb = movie.select_one('div.img-item > a > img').get('src')

                channel['movies'].append({
                    'intro': py2_encode(intro),
                    'id': movie.select_one('div.img-item > a').get('href'),
                    'label': py2_encode(label),
                    'title': py2_encode(title),
                    'realtitle': py2_encode(realtitle),
                    'thumb': thumb,
                    'type': py2_encode(type)
                })

        return channel
