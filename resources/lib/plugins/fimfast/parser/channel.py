#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }
        soup = BeautifulSoup(response, "html.parser")

        pages = soup.select('ul.pagination > li.page-item')
        if len(pages) > 2:
            channel['page'] = int(pages[-2].find(text=True, recursive=True))

        for movie in soup.select('div.tray-item > a'):
            title = py2_encode(movie.select_one('div.tray-item-title').text)
            quality = movie.select_one('span.tray-item-quality')
            if quality:
                quality = py2_encode(quality.text)

            label = "[{}] {}".format(quality, title)
            thumb = movie.select_one('img.tray-item-thumbnail').get('data-src')

            total_eps = movie.select_one('div.tray-film-likes')
            if total_eps:
                total_eps = py2_encode(total_eps.text.strip())
                label = "[{} {}] {}".format(total_eps, quality, title)

            channel['movies'].append({
                'id': movie.get('href'),
                'label': label,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'poster': thumb,
                'type': quality
            })

        return channel
