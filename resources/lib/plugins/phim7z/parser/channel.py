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
        pages = soup.select('ul.pagination > li')
        if len(pages) > 1:
            for page in pages:
                if page.select_one('a'):
                    num = re.search(r'page/(\d+)', page.select_one('a').get('href'))
                    if num and int(num.group(1)) > channel['page']:
                        channel['page'] = int(num.group(1))

        for movie in soup.select('div.ml-item > a'):
            title = movie.select_one('span.mli-info > h2').text
            mtype = movie.select_one('span.mli-eps').getText().strip()
            label = "[%s] %s" % (mtype, title)

            img = movie.select_one('img').get('src') or movie.select_one('img').get('data-original')

            movie_id = '{}/xem-phim.html'.format(movie.get('href'))
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
            return txt.encode('latin1')
        except:
            return txt.encode('utf8')
