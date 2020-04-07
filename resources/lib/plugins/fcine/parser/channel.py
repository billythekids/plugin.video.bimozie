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
        last_page = soup.select_one('ul.ipsPagination')
        print("*********************** Get pages ")
        if last_page is not None:
            page = last_page.get('data-pages')
            channel['page'] = int(page)

        for movie in soup.select('div.esnList_item > div.esnList_item_border'):
            thumb = movie.select_one('div.esnList_item_img > a > img').get('src')
            title = movie.select_one('ul.ipsDataList > li.ipsDataItem > span > a').get('title').strip()
            type = ""
            realtitle = ""

            if movie.select_one('div.cfTop') is not None:
                type = movie.select_one('div.cfTop > img').get('src').strip()
                type = re.search('ChatLuong/(.*).png', type).group(1)

            if movie.select_one('div.ipsType_light') is not None:
                realtitle = movie.select_one('div.ipsType_light').text.strip()

            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            channel['movies'].append({
                'id': movie.select_one('div.esnList_item_img > a').get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel
