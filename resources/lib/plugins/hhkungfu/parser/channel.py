# -*- coding: utf-8 -*-

import math

from bs4 import BeautifulSoup
from six.moves.html_parser import HTMLParser
from utils.xbmc_helper import text_encode

from .. import per_page


class Parser:
    # Display movies in category list
    def get(self, response, page):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        doc = BeautifulSoup(response)

        # get total page
        total_items = doc.find('opensearch:totalresults').text
        channel['page'] = math.ceil(int(total_items) / per_page)

        h = HTMLParser()
        i = 1 + ((page - 1) * per_page)
        for item in doc.findAll('entry'):
            m_type = ""
            intro = label = real_title = title = item.title.text

            soup = BeautifulSoup(h.unescape(item.content.text), "html.parser")
            image_tag = soup.select_one('img')
            thumbnail = image_tag.get('src')

            intro_tag = soup.select_one('p.noidung')
            if intro_tag:
                intro = intro_tag.text

            link = item.find(attrs={"rel": "alternate"}).get('href')
            channel['movies'].append({
                'id': link,
                'label': text_encode(label),
                'title': text_encode(title),
                'realtitle': text_encode(real_title),
                'intro': text_encode(intro),
                'thumb': thumbnail,
                'type': text_encode(m_type)
            })

            i += 1
            channel['page_patten'] = '?start-index={}&max-results={}'.format(i, per_page)

        return channel
