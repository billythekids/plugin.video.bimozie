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
        pages = soup.select('ul.page-numbers > li > a.page-numbers')
        print("*********************** Get pages ")
        if pages is not None and len(pages) > 0:
            last_page = soup.select_one('ul.page-numbers > li > a.page-numbers.next') and pages[-2] or pages[-1]
            channel['page'] = int(last_page.text)

        for tag in soup.select('div.halim_box > article'):
            movie = tag.select_one('> div.halim-item > a')
            title = movie.get('title').strip()
            thumb = movie.select_one('figure > img').get('src')



            try:
                realtitle = movie.select_one('p.original_title').text.strip().encode("utf-8")
            except:
                realtitle = title
            try:
                type = movie.select_one('span.episode').text.strip()
            except:
                type = ""
            label = "[%s] %s" % (type, title)
            try:
                intro = movie.select_one('span.status').find(text=True, recursive=False).strip()
            except:
                intro = ""

            # id = tag.get('class')[-1].replace('post-', '')
            channel['movies'].append({
                # 'id': id,
                'id': movie.get('href'),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle,
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
