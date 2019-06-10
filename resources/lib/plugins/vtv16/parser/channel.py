# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from requests.utils import quote


class Parser:
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")

        # get total page
        last_page = soup.select('div.page-navigation > span.links > a')
        print("*********************** Get pages ")
        if last_page and len(last_page) > 3:
            channel['page'] = int(last_page[-2].getText())

        for movie in soup.select('ul.list-film > li'):
            tag = movie.select_one('div.poster > a')

            if tag:
                title = tag.get('title').strip()
                thumb = tag.select_one('img').get('src')

                type = movie.select_one('div.poster > div.status').text.strip()
                label = "[%s] %s" % (type, title)
                realtitle = movie.select_one('div.name > dfn').text.strip()

                channel['movies'].append({
                    'id': tag.get('href'),
                    'label': label.encode("utf-8"),
                    'title': title.encode("utf-8"),
                    'realtitle': realtitle.encode("utf-8"),
                    'thumb': thumb,
                    'type': type.encode("utf-8")
                })

        return channel
