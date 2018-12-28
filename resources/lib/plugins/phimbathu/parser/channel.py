#!/usr/bin/env python
# coding: utf8
from bs4 import BeautifulSoup
import re


class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        last_page = soup.select('div.pagination > ul > li > a')
        print("*********************** Get pages ")
        if last_page is not None and len(last_page) > 2:
            channel['page'] = int(last_page[-2].text.strip())

        for movie in soup.select('div.film-new > ul > li'):
            title = movie.select_one('div.name > span').find(text=True, recursive=False).strip()
            type = ""
            realtitle = ""

            if movie.select_one('span.label') is not None:
                type = movie.select_one('span.label').text.strip()
            if movie.select_one('div.name-real > span') is not None:
                realtitle = movie.select_one('div.name-real > span').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            thumb = movie.select_one('img.img-film').get('data-original') or movie.select_one('img.img-film').get('src')

            movie_id = re.search("(\d+)\.html$", movie.select_one('a').get('href')).group(1)

            channel['movies'].append({
                'id': movie_id,
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel
