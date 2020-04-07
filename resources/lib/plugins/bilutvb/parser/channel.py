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

        try:
            response = response.encode('latin-1')
        except: pass

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('ul.pagination li > a')
        if pages and len(pages) > 3:
            channel['page'] = int(pages[-2].text.encode('utf8'))

        for movie in soup.select('div.movies-list > div.ml-item > a'):
            title = movie.select_one('span.mli-info > h2').find(text=True, recursive=True).encode('utf8', errors="ignore")
            mtype = ""

            episode = ' '.join(movie.select_one('span.mli-eps').find_all(text=True, recursive=True)).encode('utf8')
            label = "[{}] {}".format(episode, title)
            movie_id = movie.get('data-url')

            channel['movies'].append({
                'id': movie_id,
                'label': label,
                'title': title,
                'realtitle': title,
                'thumb': movie.select_one('img').get('data-original'),
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
