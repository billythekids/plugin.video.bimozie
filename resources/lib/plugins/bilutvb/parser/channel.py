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

        response = response.encode('latin-1')
        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('ul.page-numbers li > a.page-numbers')
        if pages and len(pages) > 3:
            channel['page'] = int(pages[-2].text.encode('utf8'))

        for movie in soup.select('div.halim_box > article.grid-item > div.halim-item > a.halim-thumb'):
            title = movie.get('title').encode('utf8', errors="ignore")
            mtype = ""

            episode = movie.select_one('span.episode')
            duration = movie.select_one('span.duration')
            if episode and duration:
                mtype = "{}/{}".format(
                    episode.text.encode('utf8'),
                    duration.find(text=True, recursive=False).encode('utf8')
                )

            realtitle = movie.select_one('p.original_title').text.encode('utf8')
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
                'thumb': movie.select_one('figure > img.lazy').get('data-src'),
                'type': mtype,
            })

        return channel

    def getSearchResult(self, response):
        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        # response = response.encode('latin-1')
        soup = BeautifulSoup(response, "html.parser")

        for movie in soup.select('li > a'):
            movie_id = movie.get('href')
            title = movie.select_one('span.label').text.encode('utf8', errors="ignore")
            realtitle = movie.select_one('span.enName').text.encode('utf8', errors="ignore")
            label = "{} - {}".format(title, realtitle)
            image = movie.select_one('img').get('src')
            mtype = ""
            
            channel['movies'].append({
                'id': movie_id,
                'label': label,
                'title': title,
                'realtitle': realtitle,
                'thumb': image,
                'type': mtype,
            })
        return channel
