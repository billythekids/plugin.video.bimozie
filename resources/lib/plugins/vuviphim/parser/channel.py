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
            tag = movie.select_one('div.poster > noscript > img')
            title = movie.select_one('div.data > h3 > a').text.strip()
            thumb = ""
            if tag and tag.get('src'):
                thumb = self.parse_url(tag.get('src').encode("utf-8"))

            try:
                type = movie.select_one('div.mepo > span.quality').text.strip()
            except:
                type = ""
            label = "[%s] %s" % (type, title)
            try:
                intro = movie.select_one('div.dtinfo > div.texto').find(text=True, recursive=False).strip()
            except:
                intro = ""

            channel['movies'].append({
                'id': movie.select_one('div.data > h3 > a').get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': title.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
                'intro': intro.encode("utf-8"),
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

        response = json.loads(response)

        for key, movie in response.iteritems():
            channel['movies'].append({
                'id': movie.get('url'),
                'label': movie.get('title'),
                'title': movie.get('title'),
                'realtitle': movie.get('title'),
                'thumb': movie.get('img'),
                'type': ''
            })

        return channel
