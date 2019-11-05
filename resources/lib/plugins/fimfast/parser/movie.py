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
        # https://fimfast.com/subtitle
        if 'subtitle' in videos and len(videos['subtitle']) > 0 and 'vi' in videos['subtitle']:
            subtitle = 'https://fimfast.com/subtitle/%s.vtt' % videos['subtitle']['vi']

        videos = videos['sources']
        if u'hls' in videos and videos['hls']:
            helper.message('Fimfast HLS', 'Movie Found')
            movie['links'].append({
                'link': videos['hls'],
                'title': 'Link hls',
                'type': 'hls',
                'resolve': False,
                'subtitle': subtitle,
                'originUrl': movieurl
            })
        elif u'hff' in videos and videos['hff'] and self.encodeString(videos['hff'], 69).find('No link') == -1:
            url = self.encodeString(videos['hff'], 69)
            movie['links'].append({
                'link': url,
                'title': 'Link hff',
                'type': 'hls',
                'resolve': False,
                'subtitle': subtitle,
                'originUrl': movieurl
            })
        else:
            for videotype in videos:
                if videos[videotype] and videotype != u'hff':
                    if type(videos[videotype]) is not unicode:
                        for key, link in enumerate(videos[videotype]):
                            movie['links'].append({
                                'link': link['src'],
                                'title': 'Link %s' % link['quality'].encode('utf-8'),
                                'type': link['type'].encode('utf-8'),
                                'resolve': True,
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
