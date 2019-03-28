# -*- coding: utf-8 -*-
import re
import json
import utils.xbmc_helper as helper
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
            subtitle = 'https://fimfast.com/subtitle/%s.vtt' % videos['subtitle']['vi']

        videos = videos['sources']
        if u'hls' in videos and videos['hls']:
            helper.message('Fimfast HLS', 'Movie Found')
            movie['links'].append({
                'link': videos['hls'],
                # 'link': self.get_hls(videos['hls']),
                'title': 'Link hls',
                'type': 'hls',
                'resolve': False,
                'subtitle': subtitle
            })
            return movie
        elif u'hff' in videos and videos['hff'] and self.encodeString(videos['hff'], 69).find('No link') == -1:
            url = self.encodeString(videos['hff'], 69)
            helper.message('Fimfast HFF', 'Movie Found')
            movie['links'].append({
                'link': url,
                # 'link': self.get_hls(url),
                'title': 'Link hff',
                'type': 'hls',
                'resolve': False,
                'subtitle': subtitle
            })
            return movie
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
                                'subtitle': subtitle
                            })
        return movie

    def get_hls(self, url):
        url = self.create_effective_playlist(url)
        return url

    def create_effective_playlist(self, url):
        play_list = ""
        base_url = urlparse(url)
        base_url = base_url.scheme + '://' + base_url.netloc
        resp = Request().get(url)
        resolutions = re.findall('RESOLUTION=\d+x(\d+)', resp)
        matches = re.findall('(/drive/.*)', resp)

        if len(resolutions) > 1:
            play_list += "#EXTM3U\n"
            if '1080' in resolutions:
                idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
                url = matches[idx]
                stream_url = base_url + url
                play_list += "#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080\n"
                play_list += "%s\n" % self.create_stream(stream_url, base_url)
            elif '720' in resolutions:
                idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
                url = matches[idx]
                stream_url = base_url + url
                play_list += "#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=1280x720\n"
                play_list += "%s\n" % self.create_stream(stream_url, base_url)
            elif '480' in resolutions:
                idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
                url = matches[idx]
                stream_url = base_url + url
                play_list += "#EXT-X-STREAM-INF:BANDWIDTH=750000,RESOLUTION=854x480\n"
                play_list += "%s\n" % self.create_stream(stream_url, base_url)
        else:
            play_list = resp
            for m in matches:
                stream_url = base_url + m
                play_list = play_list.replace(m, self.create_stream(stream_url, base_url))

        url = PasteBin().dpaste(play_list, name=url, expire=60)
        return url

    def create_stream(self, url, base_url):
        retry = 5
        res = Request()
        response = None
        while retry >= 0:
            try:
                print('Retry %d' % retry)
                response = res.get(url)
                if response != 'error': break
            except:
                pass
            finally:
                retry -= 1

        if response:
            matches = re.findall('(/drive/hls/.*)', response)
            for m in matches:
                stream_url = base_url + m
                response = response.replace(m, stream_url)

        response - response.replace('EXT-X-VERSION:5', 'EXT-X-VERSION:3')
        url = PasteBin().dpaste(response, name=url, expire=60)
        return url

    def encodeString(self, e, t):
        a = ""
        for i in range(0, len(e)):
            r = ord(e[i])
            o = r ^ t
            a += chr(o)

        return a
