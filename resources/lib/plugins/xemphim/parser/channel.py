# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json
import math
import unicodedata


class Parser:
    def get(self, response, page=1):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        response = json.loads(response)['data']['titles']

        print("*********************** Get pages ")
        if response['hasNextPage']:
            channel['page'] = math.ceil(response['total'] / 15)

        for movie in response['nodes']:
            thumb = "https://image.xemphim.plus/w342/%s" % movie["tmdbPoster"]
            label = "%s - %s" % (movie['nameVi'], movie['nameEn'])

            channel['movies'].append({
                'id': movie['id'],
                'label': label,
                'title': movie['nameVi'],
                'realtitle': movie['nameEn'],
                'thumb': thumb,
            })

        return channel

    def search_result(self, response, text):
        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        response = json.loads(response)
        text = text.encode('ascii', 'ignore').lower()
        for movie in response:
            title1 = unicodedata.normalize('NFKD', movie[1]).encode('ascii', 'ignore').lower()
            title2 = unicodedata.normalize('NFKD', movie[2]).encode('ascii', 'ignore').lower()

            if title1.find(text) > 0 or title2.find(text) > 0:
                id = movie[0]
                label = "{} {}".format(movie[2], movie[1])
                thumb = "https://image.xemphim.plus/w342/%s" % movie[3]

                channel['movies'].append({
                    'id': id,
                    'label': label,
                    'title': movie[2].encode('utf-8'),
                    'realtitle': movie[1].encode('utf-8'),
                    'thumb': thumb,
                    'type': ''
                })

        return channel
