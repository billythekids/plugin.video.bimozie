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
        pages = soup.select('ul.page-numbers li > a.page-numbers')
        if pages and len(pages) > 3:
            channel['page'] = int(pages[-2].text.encode('latin1'))

        for movie in soup.select('div.halim_box > article.grid-item > div.halim-item'):
            title = movie.select_one('h2.entry-title').text
            type = "%s/%s" % (movie.select_one('span.episode').text, movie.select_one('span.duration').find(text=True, recursive=False).strip())
            realtitle = movie.select_one('p.original_title').text
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            movie_id = movie.select_one('a.halim-thumb').get('href')

            channel['movies'].append({
                'id': movie_id,
                'label': label.encode('latin1'),
                'title': title.encode('latin1'),
                'realtitle': realtitle.encode("latin1"),
                'thumb': movie.select_one('img.lazy').get('src'),
                'type': type.encode("latin1"),
            })

        return channel
