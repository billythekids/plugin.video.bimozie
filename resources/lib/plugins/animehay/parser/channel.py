# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
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
        last_page = soup.select_one('div.ah-pagenavi > ul.pagination > li.last')
        helper.log("*********************** Get pages ")
        if last_page is not None:
            page = last_page.text.strip()
            channel['page'] = int(page)

        for movie in soup.select('div.ah-row-film > div.ah-col-film > div.ah-pad-film > a'):

            title = movie.select_one('span.name-film').find(text=True, recursive=False).strip()
            type = movie.select_one('span.number-ep-film').text.strip()
            label = "[%s] %s" % (type, title)
            thumb = movie.select_one('img').get('src')

            channel['movies'].append({
                'id': movie.get('href'),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(title),
                'thumb': thumb,
                'type': py2_encode(type)
            })

        return channel
