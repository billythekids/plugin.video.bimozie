# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
import utils.xbmc_helper as helper
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
        last_page = soup.select('div.pagination a')
        print(last_page)
        helper.log("*********************** Get pages ")

        if last_page is not None and len(last_page) > 0:
            page = re.search(r'(\d+).html', last_page[-1].get('href').strip())
            print(page)
            if page:
                channel['page'] = int(page.group(1))

        for movie in soup.select('div.movies-list > div.movie-item'):
            movie = movie.select_one('a')
            title = movie.get('title')
            mtype = movie.select_one('div.episode-latest span').text.strip()
            label = "[%s] %s" % (mtype, title)
            thumb = movie.select_one('img').get('src')

            channel['movies'].append({
                'id': movie.get('href'),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(title),
                'thumb': thumb,
                'type': py2_encode(mtype)
            })

        return channel
