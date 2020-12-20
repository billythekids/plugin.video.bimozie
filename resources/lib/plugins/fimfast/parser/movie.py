# -*- coding: utf-8 -*-
import re
import json
import utils.xbmc_helper as helper
from urlparse import urlparse
from utils.mozie_request import Request
from utils.pastebin import PasteBin


class Parser:
    def get_movie_id(self, response):
        r = re.search('data-id="(.*?)" data-episode-id="(.*?)"', response)
        fid = r.group(1)
        epid = r.group(2)

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
                'link': video['link'],
                'title': video['full_name'].encode('utf-8'),
                'thumb': video['thumbnail']
            })

        return movie

    def get_link(self, response, movieurl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        videos = json.loads(response)
        subtitle = None
        if 'subtitle' in videos and len(videos['subtitle']) > 0 and 'vi' in videos['subtitle']:
            subtitle = 'https://phim1080.me/subtitle/%s.vtt' % videos['subtitle']['vi']

        videos = videos['sources']
        for videotype in videos:
            if videos[videotype] and ('hls' in videotype or 'htt' in videotype or 'hff' in videotype):
                url = self.encodeString(videos[videotype], 69)
                movie['links'].append({
                    'link': url,
                    'title': 'Link {}'.format(videotype),
                    'type': '1080p',
                    'resolve': False,
                    'subtitle': subtitle,
                    'originUrl': movieurl
                })

            if videos[videotype] and type(videos[videotype]) is not unicode:
                for key, link in enumerate(videos[videotype]):
                    match = re.search(r'(&title=.*)&?', link['src'])
                    if match:
                        link['src'] = link['src'].replace(match.group(1), '')
                    movie['links'].append({
                        'link': link['src'],
                        'title': 'Link %s' % link['quality'].encode('utf-8'),
                        'type': link['type'].encode('utf-8'),
                        'resolve': False,
                        'subtitle': subtitle,
                        'originUrl': movieurl
                    })
        return movie

    def encodeString(self, e, t):
        a = ""
        for i in range(0, len(e)):
            r = ord(e[i])
            o = r ^ t
            a += chr(o)

        return a
