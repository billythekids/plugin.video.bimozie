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
        last_page = soup.select_one('div.PageNav')
        print("*********************** Get pages ")
        if last_page is not None:
            channel['page'] = int(last_page.get('data-last'))

        for movie in soup.select('li.discussionListItem'):
            if 'sticky' in movie.get('class'): continue
            tag = movie.select_one('div.listBlock.main a.PreviewTooltip')
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
