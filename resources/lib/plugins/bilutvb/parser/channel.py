#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


class Parser:
    def get(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('ul.page-numbers li > a.page-numbers')
        if pages and len(pages) > 3:
            channel['page'] = int(pages[-2].text.encode('utf8'))

        for movie in soup.select('div.halim_box > article.grid-item > div.halim-item > a.halim-thumb'):
            title = movie.get('title').encode('latin1', errors="ignore")
            mtype = ""

            episode = movie.select_one('span.episode')
            duration = movie.select_one('span.duration')
            if episode and duration:
                mtype = "{}/{}".format(
                    episode.text.encode('latin1', errors="ignore"),
                    duration.find(text=True, recursive=False).encode('latin1', errors="ignore")
                )

            realtitle = movie.select_one('p.original_title').text.encode('latin1', errors="ignore")
            if realtitle is not None:
                label = "[{}] {} - {}".format(mtype, title, realtitle)
            else:
                label = "[{}] {}".format(mtype, title)

            movie_id = movie.get('href')

            channel['movies'].append({
                'id': movie_id,
                'label': label,
                'title': title,
                'realtitle': realtitle,
                'thumb': movie.select_one('img.lazy').get('src'),
                'type': mtype,
            })

        return channel
