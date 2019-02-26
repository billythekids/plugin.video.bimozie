#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
from HTMLParser import HTMLParser


class Parser:
    def get_api_type(self, response):
        enable = re.search('<div class="tray-more ">', response)
        if enable:
            r = re.search('id="api-type" value="(.*)"', response)
            if r:
                return 'type', r.group(1)
            r = re.search('id="genre-slug" value="(.*)"', response)
            if r:
                return 'genre', r.group(1)

            return 'cinema', 'cinema'
        return None, None

    def get(self, response, page, api_type, api_value):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        response = json.loads(response)
        movies = response['data']
        if response['total'] > 24:
            channel['page'] = int(round(response['total']/24))
        channel['page_patten'] = '%s|%s' % (api_type, api_value)

        h = HTMLParser()
        for movie in movies:
            type = self.get_quality(int(movie['quality']))
            label = "[%s] %s" % (type, movie['name'])
            if not movie['is_movie']:
                label = "[%s/%s] %s" % (movie['meta']['max_episode_name'], movie['time'], movie['name'])

            channel['movies'].append({
                'id': movie['slug'],
                'label': label.encode("utf-8"),
                'title': movie['name'].encode("utf-8"),
                'realtitle': movie['name'].encode("utf-8"),
                'thumb': movie['thumbnail'],
                'poster': movie['poster'],
                'type': type,
                'intro': h.unescape(movie['description'])
            })

        return channel

    def get_quality(self, type):
        quality = ('SD', 'HD', 'HD')
        return quality[type-1]
