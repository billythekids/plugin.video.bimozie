from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from six.moves.urllib.parse import unquote
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

            img = Parser.extract_image(str(movie.select_one('a > img').get('data-original')))
            movie_id = movie.select_one('a').get('href')
            channel['movies'].append({
                'id': movie_id,
                'label': Parser.text(label),
                'intro': Parser.text(label),
                'title': Parser.text(title),
                'realtitle': Parser.text(title),
                'thumb': img,
                'type': Parser.text(mtype)
            })

        return channel

    @staticmethod
    def text(txt):
        try:
            return py2_encode(txt)
        except:
            return py2_encode(txt, 'latin1')

    @staticmethod
    def extract_image(url):
        match = re.search(r"url=(.*)", url)
        if match:
            return unquote(match.group(1))

        return url
