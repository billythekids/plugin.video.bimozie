# -*- coding: utf-8 -*-
import re
import json


class Parser:
    def get_movie_id(self, response):
        r = re.search('data-id="(.*)" data-episode-id="(.*)"', response)
        fid = int(r.group(1))
        epid = int(r.group(2))

        return fid, epid

    def get(self, response, fid):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        movies = json.loads(response)['data']
        movie['group']['fimfast'] = []
        for video in movies:
            movie['group']['fimfast'].append({
                    # 'link': '%s,%s' % (fid, video['id']),
                    'link': video['link'],
                    'title': video['full_name'].encode('utf-8'),
                    'thumb': video['thumbnail']
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        videos = json.loads(response)
        subtitle = None
        # https://fimfast.com/subtitle
        if 'subtitle' in videos and len(videos['subtitle']) > 0 and 'vi' in videos['subtitle']:
            subtitle = 'https://fimfast.com/subtitle/%s' % videos['subtitle']['vi']

        videos = videos['sources']
        for videotype in videos:
            if videos[videotype]:
                if type(videos[videotype]) is not unicode:
                    for key, link in enumerate(videos[videotype]):
                        movie['links'].append({
                            'link': link['src'],
                            'title': 'Link %s' % link['quality'].encode('utf-8'),
                            'type': link['type'].encode('utf-8'),
                            'resolve': True,
                            'subtitle': subtitle
                        })
                else:
                    movie['links'].append({
                        'link': videos[videotype],
                        'title': 'Link %s' % videotype.encode('utf-8'),
                        'type': videotype.encode('utf-8'),
                        'resolve': False,
                        'subtitle': subtitle
                    })

        return movie
