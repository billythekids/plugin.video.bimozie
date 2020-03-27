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
                mtype = dom.select_one('> span.status').text
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
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': img,
                'type': mtype.encode("utf-8"),
            })

        return channel
