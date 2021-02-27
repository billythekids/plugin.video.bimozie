# -*- coding: utf-8 -*-
from utils.xbmc_helper import humanbytes


class Parser:
    # Display movies in category list
    def get(self, response, page=1):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        for movie in response:
            title = movie.get('name')
            thumbnail = ""
            link = 'https://www.fshare.vn/{}/{}'.format(int(movie.get('type')) == 0 and 'folder' or 'file', movie.get('linkcode'))

            if int(movie.get('deleted')) > 0:
                continue
            if int(movie.get('size')) > 0:
                title = '[%s] %s' % (humanbytes(movie.get('size')), title)

            channel['movies'].append({
                'intro': title,
                'isFolder': int(movie.get('type')) == 0 and True or False,
                'id': link,
                'code': movie.get('linkcode'),
                'link': link,
                'label': title,
                'title': title,
                'realtitle': title,
                'thumb': thumbnail,
                'type': 'Fshare',
                'resolve': False
            })

        return channel
