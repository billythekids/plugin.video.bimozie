import re

from bs4 import BeautifulSoup
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
        for page in soup.select('div.pagination a'):
            if page.get('class') is None or 'navigation' not in page.get('class'):
                try:
                    channel['page'] = int(page.text)
                except:
                    pass

        for movie in soup.select('ul.list-film > li > div'):
            title = movie.select_one('p.name')
            if title:
                title = title.text
            elif movie.select_one('div.title'):
                title = movie.select_one('div.title').text
            m_type = movie.select_one('label')
            if m_type:
                m_type = m_type.text
            realtitle = movie.select_one('.real-name')
            if realtitle:
                realtitle = realtitle.text

            if realtitle is not None:
                label = "[%s] %s - %s" % (m_type, title, realtitle)
            else:
                label = "[%s] %s" % (m_type, title)

            img = movie.select_one('div.list-img').get('style')
            img = re.search(r"background-image:url\((.*)\)", img).group(1)

            if 'https://' not in img:
                img = 'https://{}'.format(img)

            # movie_id = re.search(r"((\d{2,}))", movie.select_one('a').get('href')).group(1)
            channel['movies'].append({
                'id': movie.select_one('a').get('href'),
                'label': py2_encode(label),
                'title': py2_encode(title),
                'realtitle': py2_encode(realtitle),
                'thumb': img,
                'type': py2_encode(m_type),
            })

        return channel
