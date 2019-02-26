# -*- coding: utf-8 -*-
import re
import json
from urlparse import urlparse
from utils.mozie_request import Request
from utils.pastebin import PasteBin


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
                        'link': self.get_hls(videos[videotype]),
                        'title': 'Link %s' % videotype.encode('utf-8'),
                        'type': videotype.encode('utf-8'),
                        'resolve': True,
                        'subtitle': subtitle
                    })
        return movie

    def get_hls(self, url):
        url = self.create_effective_playlist(url)
        return url

    def create_effective_playlist(self, url):
        base_url = urlparse(url)
        base_url = base_url.scheme + '://' + base_url.netloc
        resp = Request().get(url)
        matches = re.findall('(/drive/.*)', resp)

        for m in matches:
            stream_url = base_url + m
            resp = resp.replace(m, self.create_stream(stream_url, base_url))

        url = PasteBin().dpaste(resp, name=url, expire=60)
        return url

    def create_stream(self, url, base_url):
        retry = 5
        res = Request()
        response = None
        while retry >= 0:
            try:
                response = res.get(url)
                if response != 'error':
                    break
            except:
                pass
            finally:
                retry -= 1

        if response:
            matches = re.findall('(/drive/hls/.*)', response)
            for m in matches:
                stream_url = base_url + m
                response = response.replace(m, stream_url)

            url = PasteBin().dpaste(response, name=url, expire=60)
            return url
