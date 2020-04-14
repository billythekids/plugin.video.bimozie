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
        for page in soup.select('div.pagination a'):
            if page.get('class') is None or 'navigation' not in page.get('class'):
                try:
                    channel['page'] = int(page.text)
                except:
                    pass

        for movie in soup.select('div.left-content > div.block-film > ul.list-film > li.film-item'):
            title = movie.select_one('p.name').text
            type = movie.select_one('label').text
            realtitle = movie.select_one('p.real-name').text
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            movie_id = re.search("(\d+)\.html$", movie.select_one('a').get('href')).group(1)
            channel['movies'].append({
                'id': movie_id,
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': movie.select_one('img').get('src'),
                'type': type.encode("utf-8"),
            })

        return channel
