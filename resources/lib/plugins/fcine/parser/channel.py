# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from kodi_six.utils import py2_encode
import utils.xbmc_helper as helper


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
        helper.log("*********************** Get pages ")
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
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': thumb,
                'type': py2_encode(type)
            })

        return channel
