from bs4 import BeautifulSoup
import re
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        for page in soup.select('ul.page-numbers > li > a'):
            page = re.search(r'trang-(\d+)', page.get('href'))
            if page:
                try:
                    channel['page'] = int(page.group(1))
                except:
                    pass

        for movie in soup.select('div.grid-item > div.xpo-item'):
            dom = movie.select_one('a.xpo-thumb')
            title = dom.get('title')
            mtype = ""
            try:
                mtype = dom.select_one('span.status').text
            except: pass
            realtitle = movie.select_one('p.original_title').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (mtype, title, realtitle)
            else:
                label = "[%s] %s" % (mtype, title)

            img = movie.select_one('img.lazy').get('src')

            movie_id = movie.select_one('a.xpo-thumb').get('href')
            channel['movies'].append({
                'id': movie_id,
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': img,
                'type': py2_encode(mtype),
            })

        return channel
