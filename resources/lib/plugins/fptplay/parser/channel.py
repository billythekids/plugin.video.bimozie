# -*- coding: utf-8 -*-
import re
import json
from bs4 import BeautifulSoup


class Parser:
    def get(self, response, page=1, domain=''):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        channel['page'] = 2

        for movie in soup.select('#main-content div.block div.block-content > div.row div.global-figure > a'):
            thumb = self.get_thumb(str(movie))
            title = movie.get('data-ctn').encode('utf-8')

            movie = {
                'id': movie.get('data-ela'),
                'label': title,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'type': None
            }

            channel['movies'].append(movie)

        return channel

    def get_page_ajax(self, response, page=2, domain=''):
        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        response = json.loads(response)

        channel['page'] = response['total_page']

        for movie in response['videos_list']:
            channel['movies'].append({
                # 'id': id,
                'id': movie['_id'],
                'label': movie['title'].encode("utf-8"),
                'title': movie['title_vie'].encode("utf-8"),
                'realtitle': movie['title_origin'],
                'thumb': movie['thumb'],
                'type': movie['duration'].encode("utf-8"),
                'intro': movie['description'].encode("utf-8"),
            })

        return channel

    def get_thumb(self, style):
        return re.search('background-image:url\((.*?)\)', style).group(1)

    def get_search(self, response, page=1):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        last_page = soup.select_one('div.PageNav')
        print("*********************** Get pages ")
        if last_page is not None:
            channel['page'] = int(last_page.get('data-last'))

        for movie in soup.select('li.searchResult'):
            tag = movie.select_one('div.listBlock.main div.titleText > h3.title > a')
            title = tag.text.strip().encode("utf-8")
            thumb = None

            channel['movies'].append({
                'id': tag.get('href'),
                'label': title,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'type': None
            })

        return channel
