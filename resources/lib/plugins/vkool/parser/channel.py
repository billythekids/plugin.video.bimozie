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
        pages = soup.select('ul.pagination > li > a')
        for page in pages:
            try:
                channel['page'] = int(re.search("/(\d+)\.html$", page.get('href')).group(1))
            except: pass

        for movie in soup.select('ul.list-movie > li.movie-item > a'):
            title = movie.select_one('span.movie-title-1').text
            type = movie.select_one('span.ribbon').text
            realtitle = movie.select_one('span.movie-title-2').text
            thumb = re.search(r':url\((.*?)\);', movie.select_one('div.movie-thumbnail').get('style')).group(1)

            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            movie_id = re.search("(\d+)\.html$", movie.get('href')).group(1)
            channel['movies'].append({
                'id': movie_id,
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumb,
                'type': type.encode("utf-8"),
            })

        return channel
