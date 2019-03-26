# -*- coding: utf-8 -*-
import re
import HTMLParser
import json
import urllib
import utils.xbmc_helper as helper
from utils.mozie_request import Request, AsyncRequest
from utils.fshare import FShare
from utils.pastebin import PasteBin


def rsl(s):
    s = str(s).replace('HDG', '') \
        .replace('HD', '1080') \
        .replace('SD', '640') \
        .replace('large', '640') \
        .replace('lowest', '240') \
        .replace('low', '480') \
        .replace('hd', '720') \
        .replace('fullhd', '1080') \
        .replace('Auto', '640') \
        .replace('medium', '240') \
        .replace('mobile', '240') \
        .replace('AUTO', '640')

    result = re.search('(\d+)', s)
    if result:
        return result.group(1)
    else:
        return '240'


class LinkParser:
    def __init__(self, media):
        self.media = media
        self.url = media['link']

    def get_link(self):
        print("Find link source of %s" % self.url)
        if re.search('ok.ru', self.url):
            self.url.replace('?autoplay=1', '')
            return self.get_link_ok()
        if re.search('openload.co', self.url):
            return self.get_link_openload()
        if re.search('fshare.vn', self.url):
            return self.get_link_fshare()
        if re.search('dailymotion.com', self.url):
            return self.get_link_dailymotion()
        if self.url.endswith('m3u8'):
            return self.get_m3u8()
        if re.search('fptplay.net', self.url):
            return self.get_fptplay()
        if re.search('sstreamgg.xyz', self.url) or re.search('ggstream.me', self.url) or re.search('tstream.xyz',
                                                                                                   self.url):
            return self.get_sstreamgg()
        if re.search('hls.phimmoi.net', self.url):
            return self.get_hls_phimmoi()
        if re.search('phimmoi.net/hydrax.html', self.url):
            return self.get_hydrax_phimmoi()
        if re.search('youtube.com', self.url):
            return self.get_youtube()

        return self.url, 'unknow'

    def get_link_ok(self):
        response = Request().get(self.url)
        m = re.search('data-options="(.+?)"', response)
        h = HTMLParser.HTMLParser()
        s = m.group(1)
        s = h.unescape(s)
        s = json.loads(s)
        s = json.loads(s['flashvars']['metadata'])
        items = [(i['url'], rsl(i['name'])) for i in s['videos']]
        items = sorted(items, key=lambda elem: int(elem[1]), reverse=True)
        return items[0]

    def get_youtube(self):
        self.url = self.url.replace(re.search('^http.*(\?.*)', self.url).group(1), '')
        try:
            import resolveurl
            re.sub('(^http.*)\?', '\1', self.url)
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_openload(self):
        try:
            import resolveurl
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_dailymotion(self):
        try:
            import resolveurl
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_fshare(self):
        if not helper.getSetting('fshare.username'):
            helper.message('Required username/password to get fshare.vn link, open addon settings', 'Login Required')

        if helper.getSetting('fshare.enable'):
            return FShare(
                self.url,
                helper.getSetting('fshare.username'),
                helper.getSetting('fshare.password')
            ).get_link(), '1080'
        else:
            return FShare(self.url).get_link(), '1080'

    def get_m3u8(self):
        # support to run with inputstream.adaptive
        if re.search('51.15.90.176', self.url):  # skip this for phimbathu & bilutv
            return self.url, 'hls5'

        return self.url, 'hls'

    def get_fptplay(self):
        base_url = self.url.rpartition('/')[0]
        res = Request()
        response = res.get(self.url)
        matches = re.findall('(chunklist.*)', response)

        stream_urls = []
        for m in matches:
            stream_url = base_url + '/' + m
            stream_urls.append((stream_url, m))

        arequest = AsyncRequest(res)
        results = arequest.get(list(map(lambda x: x[0], stream_urls)), parser=self.parse_fptplay_stream, args=base_url)
        for i in range(len(stream_urls)):
            response = response.replace(stream_urls[i][1], results[i])

        url = PasteBin().dpaste(response, name=self.url, expire=60)
        return url, '1080'

    @staticmethod
    def parse_fptplay_stream(response, request, base_url):
        matches = re.findall('(media_.*)', response)
        for m in matches:
            stream_url = base_url + '/' + m
            response = response.replace(m, stream_url)

        url = PasteBin().dpaste(response, name=base_url, expire=60)
        return url

    @staticmethod
    def __get_fptplay_stream(url, base_url):
        response = Request().get(url)
        matches = re.findall('(media_.*)', response)

        for m in matches:
            stream_url = base_url + '/' + m
            response = response.replace(m, stream_url)

        url = PasteBin().dpaste(response, name=url, expire=60)
        return url

    def get_sstreamgg(self):
        url = self.url + "|Referer=https://vuviphim.com/"
        return url, '720'

    def get_hls_phimmoi(self):
        req = Request()
        response = req.get(self.url)

        # found playlist
        if re.search('EXT-X-STREAM-INF', response):
            resolutions = re.findall('RESOLUTION=\d+x(\d+)', response)
            matches = re.findall('(http.*)\r', response)
            if '1080' in resolutions:
                idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
                url = matches[idx]
            elif '720' in resolutions:
                idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
                url = matches[idx]
            elif '480' in resolutions:
                idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
                url = matches[idx]

            response = Request().get(url, headers={
                'origin': 'http://www.phimmoi.net'
            })

        links = re.findall('(https?://(?!so-trym).*)\r', response)
        if links:
            media_type = 'hls4'
            arequest = AsyncRequest(request=req, retry=2)
            results = arequest.head(links, headers={
                'origin': 'http://www.phimmoi.net',
                'referer': self.media['origin_url']
            }, redirect=False)

            for i in range(len(links)):
                try:
                    response = response.replace(links[i], results[i].headers['location'])
                except:
                    print(links[i], results[i].headers)
        else:
            media_type = 'hls'

        stream_url = PasteBin().dpaste(response, name=self.url, expire=60)
        playlist = "#EXTM3U\n#EXT-X-VERSION:3\n"
        playlist += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
        playlist += "%s\n" % stream_url
        url = PasteBin().dpaste(playlist, name=self.url, expire=60)
        if 'hls' == media_type:
            url += '|referer=' + urllib.quote_plus(self.media['origin_url'])

        return url, media_type

    def get_hydrax_phimmoi(self):
        response = Request().get(self.url)
        token = re.search('"key":"(.*?)",', response).group(1)
        params = {
            'key': token,
            'type': 'slug',
            'value': re.search('#slug=(.*)', self.url).group(1)
        }
        response = Request().post('https://multi.hydrax.net/vip', params, {
            'Origin': 'http://www.phimmoi.net',
            'Referer': 'http://www.phimmoi.net/hydrax.html'
        })

        response = json.loads(response)
        r = "#EXTM3U\n#EXT-X-VERSION:3\n"
        if 'hd' in response:
            r += "#EXT-X-STREAM-INF:BANDWIDTH=1998000,RESOLUTION=1280x720\n"
            r += "%s\n" % self.get_hydrax_phimmoi_stream(response['hd'], response['servers'])
        elif 'fullhd' in response:
            r += "#EXT-X-STREAM-INF:BANDWIDTH=2998000,RESOLUTION=1920x1080\n"
            r += "%s\n" % self.get_hydrax_phimmoi_stream(response['fullhd'], response['servers'])
        elif 'mhd' in response:
            r += "#EXT-X-STREAM-INF:BANDWIDTH=996000,RESOLUTION=640x480\n"
            r += "%s\n" % self.get_hydrax_phimmoi_stream(response['mhd'], response['servers'])
        elif 'sd' in response:
            r += "#EXT-X-STREAM-INF:BANDWIDTH=394000,RESOLUTION=480x360\n"
            r += "%s\n" % self.get_hydrax_phimmoi_stream(response['sd'], response['servers'])
        elif 'origin' in response:
            r += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
            r += "%s\n" % self.get_hydrax_phimmoi_stream(response['origin'], response['servers'])

        url = PasteBin().dpaste(r, name=self.url, expire=60)
        return url, 'hls4'

    @staticmethod
    def get_hydrax_phimmoi_stream(stream, n):
        txt = "#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:" + stream[
            'duration'] + "\n#EXT-X-MEDIA-SEQUENCE:0\n"
        links = []

        r = len(stream['range'])
        o = len(n)
        a = stream['expired']
        s = 0
        if stream['type'] == 2:
            r = 0
            l = stream['multiRange']
            h = len(l)

            for t in range(h):
                u = stream['multiData'][t]['file']
                f = 0
                p = 0

                for d in range(len(l[t])):
                    if s < o:
                        c = n[s]
                        s += 1
                    else:
                        s = 1
                        c = n[0]

                    txt += "#EXTINF:%s,\n" % stream['extinf'][r]
                    txt += "#EXT-X-BYTERANGE:%s\n" % l[t][d]

                    y = l[t][d]

                    c = "http://" + c + "/" + stream['id'] + "/" + stream['range'][t]
                    if '@' in l[t][d]:
                        g, y = l[t][d].split('@')
                        g, y = int(g), int(y)
                        if not g or not y: continue
                        f = d and p + 1 or y
                        p = y and f + g - 1 or g - 1
                        y = '%s-%s' % (f, p)

                    url = a and c + "/" + a + "/" + u or c + "/" + r + "/" + u
                    url += stream['id'] and "/" + y + ".js" or "/" + y + ".jpg"
                    links.append(url)
                    txt += url + "\n"
                    r += 1
                if h == t + 1:
                    txt += "#EXT-X-ENDLIST"

        arequest = AsyncRequest()
        results = arequest.head(links, headers={
            'origin': 'http://www.phimmoi.net'
        })

        media_urls = list()
        for i in range(len(links)):
            try:
                media_url = results[i].headers['location']
                txt = txt.replace(links[i], media_url)
                media_urls.append(media_url)
            except:
                print(links[i])

        url = PasteBin().dpaste(txt, name=stream['id'], expire=60)
        return url
