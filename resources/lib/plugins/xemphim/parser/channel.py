# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json
import unicodedata


class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        last_page = soup.select('ul.pagination-list > li > a.pagination-link')
        print("*********************** Get pages ")
        if last_page is not None and len(last_page) > 0:
            last_page = last_page[-1]
            page = last_page.text.strip()
            channel['page'] = int(page)

        for movie in soup.select('div.grid.columns > div.column'):
            title = movie.select_one('h3.name.vi > a').text.strip()
            realtitle = movie.select_one('h3.name.en > a').text.strip()
            thumb = movie.select_one('> a > img').get('src')

            label = "%s - %s" % (title, realtitle)

            channel['movies'].append({
                'id': movie.select_one('h3.name.vi > a').get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
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
                id = "/movie/%s~%s" % (movie[1].replace(' ', '-').encode('utf-8').lower(), movie[0])
                label = "%s %s" % (movie[2].encode('utf-8'), movie[1].encode('utf-8'))
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
