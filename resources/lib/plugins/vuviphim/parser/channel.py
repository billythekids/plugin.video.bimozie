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
        last_page = soup.select_one('div.pagination > span')
        print("*********************** Get pages ")
        if last_page is not None:
            page = re.search('Page \d+ of (\d+)', last_page.text.strip()).group(1)
            channel['page'] = int(page)

        for movie in soup.select('div.module > div.content > div.items > article.item'):
            tag = movie.select_one('div.poster > a > img')
            title = tag.get('alt').strip()
            thumb = self.parse_url(tag.get('src').encode("utf-8"))

            type = movie.select_one('div.poster > span.quality').text.strip()
            label = "[%s] %s" % (type, title)
            try:
                intro = movie.select_one('div.dtinfo > div.texto').find(text=True, recursive=False).strip()
            except:
                intro = ""

            channel['movies'].append({
                'id': movie.select_one('div.poster > a').get('href'),
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

        soup = BeautifulSoup(response, "html.parser")
        for movie in soup.select('div.asp_r_pagepost'):
            tag = movie.select_one('div.asp_content > h3 > a')
            title = tag.find(text=True, recursive=False).strip().encode("utf-8")
            thumb = movie.select_one('a.asp_res_image_url > div.asp_image').get('style')
            thumb = re.search("\('(http.*?)'\);", thumb).group(1)

            channel['movies'].append({
                'id': tag.get('href'),
                'label': title,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'type': ''
            })

        return channel
