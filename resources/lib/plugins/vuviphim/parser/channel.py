# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re, json
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
        last_page = soup.select_one('div.pagination > span')
        print("*********************** Get pages ")
        if last_page is not None:
            page = re.search('Page \d+ of (\d+)', last_page.text.strip()).group(1)
            channel['page'] = int(page)

        for movie in soup.select('div.module > div.content > div.items > article.item'):
            tag = movie.select_one('div.poster > img')
            title = movie.select_one('div.data > h3 > a').text.strip()
            thumb = ""
            if tag and tag.get('src'):
                thumb = self.parse_url(tag.get('src'))

            try:
                type = movie.select_one('div.mepo > span.quality').text.strip()
            except:
                type = ""
            label = "[%s] %s" % (type, title)
            try:
                intro = movie.select_one('div.dtinfo > div.texto').find(text=True, recursive=False).strip()
            except:
                intro = label

            channel['movies'].append({
                'id': movie.select_one('div.data > h3 > a').get('href'),
                'label': label,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'type': type,
                'intro': intro,
            })

        return channel

    def parse_url(self, url):
        url = quote(url).replace('%3A', ':')

        return url

    def search_result(self, response):
        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }
        soup = BeautifulSoup(response, "html.parser")
        for movie in soup.select('div.search-page > div.result-item'):
            tag = movie.select_one('div.image img')
            title = movie.select_one('div.details > div.title > a').text.strip()
            thumb = ""
            if tag and tag.get('src'):
                thumb = self.parse_url(tag.get('src'))

            try:
                type = movie.select_one('div.image a > span.post').text.strip()
            except:
                type = ""
            label = "[%s] %s" % (type, title)
            try:
                intro = movie.select_one('div.contenido').find(text=True, recursive=False).strip()
            except:
                intro = label

            channel['movies'].append({
                'id': movie.select_one('div.details > div.title > a').get('href'),
                'label': label,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'type': type,
                'intro': intro,
            })

        return channel
