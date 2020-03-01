# -*- coding: utf-8 -*-
import re
import json


class Parser:

    def get(self, response, mid):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        data = re.search(r'__NUXT__=(.*?);</script>', response)
        if not data:
            return movie

        data = json.loads(data.group(1))

        server_name = 'Fptplay'
        movie['group'][server_name] = []
        i = 0
        for ep in data['data'][0]['result']['episodes']:
            if ep['is_trailer'] == 0:
                url = '%s/%s' % (mid, i)
                movie['group'][server_name].append({
                    'link': url,
                    'title': ep['title'].encode('utf-8'),
                    'thumb': ep['thumb'],
                    'type': '',
                    'resolve': False
                })
            i += 1

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        data = json.loads(response)
        if 'data' in data:
            data = data['data']
            movie['links'].append({
                'link': data['url'],
                'title': 'Link %s' % data['name'].encode('utf-8'),
                'type': 'hls',
                'resolve': False
            })

        return movie
