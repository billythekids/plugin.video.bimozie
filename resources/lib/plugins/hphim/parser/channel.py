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
