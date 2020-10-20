from bs4 import BeautifulSoup
import re


class Parser:
    def get(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('div.pagination > ul > li')
        if len(pages) > 1:
            for page in pages:
                if page.select_one('a'):
                    num = page.select_one('a').text
                    if num.isnumeric() and int(num) > channel['page']:
                        channel['page'] = int(num)

        for movie in soup.select('div.list-films > ul > li'):
            title = movie.select_one('a').get('title')
            mtype = movie.select_one('span.label').text
            label = "[%s] %s" % (mtype, title)

            img = movie.select_one('a > img').get('src')
            movie_id = movie.select_one('a').get('href')
            channel['movies'].append({
                'id': movie_id,
                'label': Parser.text(label),
                'title': Parser.text(title),
                'realtitle': Parser.text(title),
                'thumb': img,
                'type': Parser.text(mtype)
            })

        return channel

    @staticmethod
    def text(txt):
        try:
            return txt.encode('utf8')
        except:
            return txt.encode('latin1')
