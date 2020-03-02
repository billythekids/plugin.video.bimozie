# -*- coding: utf-8 -*-
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
        last_page = soup.select('p.pages > a.pagelink')
        print("*********************** Get pages ")
        if len(last_page) > 1:
            channel['page'] = int(last_page[-1].text.strip())

        for movie in soup.select('ul.list-movie > li.movie-item > a.block-wrapper'):
            tag = movie.select_one('div.movie-meta')
            title = tag.select_one('span.movie-title-1').text.strip()
            realtitle = tag.select_one('span.movie-title-2').text.strip()
            thumb = re.search(r':url\((.*?)\);', movie.select_one('div.movie-thumbnail').get('style')).group(1)

            type = tag.select_one('span.movie-title-chap').text.strip()
            label = "[%s] %s" % (type, title)
            intro = ""

            channel['movies'].append({
                'id': movie.get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
                'intro': intro.encode("utf-8"),
            })

        return channel

    def getTop(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")

        for movie in soup.select('li > a.movie-item'):
            title = movie.select_one('div.movie-title-1').text.strip()
            realtitle = type = ""
            if movie.select_one('span.ribbon') is not None:
                type = movie.select_one('span.ribbon').text.strip()
            if movie.select_one('span.movie-title-2') is not None:
                realtitle = movie.select_one('span.movie-title-2').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            thumb =  re.search(r"background-image:url\('(.*)'\)", movie.select_one('div.public-film-item-thumb').get('style')).group(1)

            channel['movies'].append({
                'id': movie.get('href').encode("utf-8"),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel

    def search_result(self, response):
        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        try:
            soup = BeautifulSoup(response, "html.parser")
            for movie in soup.select('li.movie-item'):
                tag = movie.select_one('> a')
                title = tag.get('title').strip().encode("utf-8")
                thumb = re.search(r':url\((.*?)\);', movie.select_one('div.movie-thumbnail').get('style')).group(1)

                channel['movies'].append({
                    'id': tag.get('href'),
                    'label': title,
                    'title': title,
                    'realtitle': title,
                    'thumb': thumb,
                    'type': ''
                })
        except: pass

        return channel
