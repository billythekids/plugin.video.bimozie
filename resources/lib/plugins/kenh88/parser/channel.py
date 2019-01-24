#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re


class Parser:
    def get(self, response, page, domain):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('ul.pagination > li > a')
        print("*********************** Get pages ")
        try:
            if pages and len(pages) > 1:
                page = pages[-1]
                channel['page'] = int(page.text.encode('utf-8'))
        except:
            pass

        for movie in soup.select('div#list-1 > div.row > div'):
            title = movie.select_one('h2 > a').text.strip()
            type = ''

            if movie.select_one('span.status'):
                type = movie.select_one('span.status').text.strip()

            if movie.select_one('span.process > span.process_r'):
                type = '%s - %s' % (type, movie.select_one('span.process > span.process_r').text.strip())

            realtitle = movie.select_one('h2 > a').find(text=True, recursive=False).strip()
            label = "[%s] %s - %s" % (type, title, realtitle)
            thumb = "%s/%s" % (domain, movie.select_one('a > img').get('src'))

            channel['movies'].append({
                'id': movie.select_one('h2 > a').get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel
