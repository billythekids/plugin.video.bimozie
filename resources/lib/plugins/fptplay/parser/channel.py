# -*- coding: utf-8 -*-
import re
import json
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response, page=1, domain=''):
        channel = {'page': 2, 'page_patten': None, 'movies': []}

        data = re.search(r'__NUXT__=(.*?);</script>', response)
        if not data:
            return channel

        data = json.loads(data.group(1))['data'][0]
        for movie in data['vods']:
            channel['movies'].append({
                'id': movie['_id'],
                'label': py2_encode(movie['title']),
                'title': py2_encode(movie['title_vie'] or movie['title']),
                'realtitle': py2_encode(movie['title_origin']),
                'thumb': movie['thumb'],
                'type': '',
                'intro': py2_encode(movie['description']),
            })

        return channel

    def get_page_ajax(self, response, page=2, domain=''):
        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        response = json.loads(response)

        channel['page'] = response['total_page']

        for movie in response['videos_list']:
            channel['movies'].append({
                # 'id': id,
                'id': movie['_id'],
                'label': py2_encode(movie['title']),
                'title':  py2_encode(movie['title']),
                'realtitle': movie['title_origin'],
                'thumb': movie['thumb'],
                'type': py2_encode(movie['duration']),
                'intro': py2_encode(movie['description']),
            })

        return channel

    def get_thumb(self, style):
        return re.search('background-image:url\((.*?)\)', style).group(1)

    def get_search(self, response):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        data = re.search(r'__NUXT__=(.*?);</script>', response)

        if not data:
            return channel

        data = json.loads(data.group(1))['data'][0]
        for movie in data['searchData']:
            channel['movies'].append({
                'id': movie['_id'],
                'label': py2_encode(movie['title']),
                'title': py2_encode(movie['title_vie'] or movie['title']),
                'realtitle': py2_encode(movie['title_origin']),
                'thumb': movie['thumb'],
                'type': '',
                'intro': '',
            })
        return channel
