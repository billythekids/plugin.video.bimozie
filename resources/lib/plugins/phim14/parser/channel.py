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
        pages = soup.select('div.navpage > span.item > a')
        print("*********************** Get pages ")
        try:
            if pages and len(pages) > 1:
                page = pages[-1]
                channel['page'] = int(page.text.encode('utf-8'))
        except:
            pass

        for movie in soup.select('ul.list-film > li > div.inner'):
            title = movie.select_one('div.info > h2 > a').get('title').strip()
            type = ''

            if movie.select_one('div.status > span.status_r'):
                type = movie.select_one('div.status > span.status_r').text.strip()
            else:
                type = movie.select_one('div.status').text.strip()

            if movie.select_one('span.process > span.process_r'):
                type = '%s - %s' % (type, movie.select_one('span.process > span.process_r').text.strip())

            realtitle = movie.select_one('div.info > div.name2').text.strip()
            label = "[%s] %s" % (type, title)
            thumb = movie.select_one('a > img').get('src').replace('/thumb', '')

            channel['movies'].append({
                'id': movie.select_one('h2 > a').get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': title.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel
