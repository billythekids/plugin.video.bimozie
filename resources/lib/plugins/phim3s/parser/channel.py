#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import json


class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        last_page = soup.select('span.page_nav > span.item > a')
        print("*********************** Get pages ")
        if last_page is not None and len(last_page) > 2:
            channel['page'] = int(last_page[-2].text.strip())

        for movie in soup.select('ul.list-film > li > div.inner'):
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

            thumb = movie.select_one('a img').get('src')

            channel['movies'].append({
                'id': movie.select_one('div.name > a').get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel

    def search(self, response, page=1):
        results = json.loads(response)
        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        for key in results['json']:
            result = results['json'][key]
            label = "[%s] %s - %s" % (result['status'], result['title'], result['title_o'])
            channel['movies'].append({
                'id': result['link'],
                'label': label.encode("utf-8"),
                'title': result['title'].encode("utf-8"),
                'realtitle': result['title_o'].encode("utf-8"),
                'thumb': result['thumb_url'],
                'type': result['status'].encode("utf-8"),
            })

        return channel
