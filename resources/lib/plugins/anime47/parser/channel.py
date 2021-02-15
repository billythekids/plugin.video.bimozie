# coding=latin1
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
        pages = soup.select_one('ul.pagination')

        print("*********************** Get pages ")
        m = re.findall(r'(page)?[/|=](\d+)(.html)?', str(pages))
        if m:
            m = [int(x[1]) for x in m]
            channel['page'] = max(m)

        for movie in soup.select('ul#movie-last-movie > li a'):
            realtitle = ""
            title = movie.select_one('div.movie-title-1').text.strip()
            type = ""
            if movie.select_one('span.ribbon') is not None:
                type = movie.select_one('span.ribbon').text.strip()
            if movie.select_one('span.movie-title-2') is not None:
                realtitle = movie.select_one('span.movie-title-2').text.strip()

            if realtitle:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                realtitle = title
                label = "[%s] %s" % (type, title)

            thumb = re.search(r"background-image:url\('(.*)'\)",
                              movie.select_one('div.public-film-item-thumb').get('style')).group(1)

            channel['movies'].append({
                'id': movie.get('href').encode("latin1"),
                'label': label.encode("latin1"),
                'title': title.encode("latin1"),
                'realtitle': realtitle.encode("latin1"),
                'thumb': thumb,
                'type': type.encode("latin1"),
            })

        return channel

    def getTop(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")

        for movie in soup.select('li > a.movie-item'):
            title = movie.select_one('div.movie-title-1').text.strip()
            realtitle = type = ""
            if movie.select_one('span.ribbon') is not None:
                type = movie.select_one('span.ribbon').text.strip()
            if movie.select_one('span.movie-title-2') is not None:
                realtitle = movie.select_one('span.movie-title-2').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            thumb = re.search(r"background-image:url\('(.*)'\)",
                              movie.select_one('div.public-film-item-thumb').get('style')).group(1)

            channel['movies'].append({
                'id': movie.get('href').encode("latin1"),
                'label': label.encode("latin1"),
                'title': title.encode("latin1"),
                'realtitle': realtitle.encode("latin1"),
                'thumb': thumb,
                'type': type.encode("latin1"),
            })

        return channel
