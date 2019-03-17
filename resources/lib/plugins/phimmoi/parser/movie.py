# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.mozie_request import AsyncRequest
from utils.aes import CryptoAES
from utils.pastebin import PasteBin
import re
import json
import requests


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get(self, response, url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        self.originURL = url

        # get episode if possible
        servers = soup.select('div.list-server > div.server')
        if skipEps is False and len(servers) > 0:
            print("***********************Get Movie Episode*****************************")
            found = False
            items = self.get_server_list(servers)
            if items is not None and len(items) > 0:
                movie['group'] = items
                found = True
            else:
                found = False
            if found is False:
                servers = soup.select('ul.server-list > li.backup-server')
                movie['group'] = self.get_server_list(servers)

        else:
            print("***********************Get Movie Link*****************************")
            url = self.get_token_url(response)
            response = Request().get(url)

            self.key = self.get_decrypt_key(response)
            jsonresponse = re.search("_responseJson='(.*)';", response).group(1)
            jsonresponse = json.loads(jsonresponse.decode('utf-8'))

            if jsonresponse['medias']:
                media = sorted(jsonresponse['medias'], key=lambda elem: elem['resolution'], reverse=True)
                for item in media:
                    url = CryptoAES().decrypt(item['url'], bytes(self.key.encode('utf-8')))
                    if not re.search('hls.phimmoi.net', url):
                        movie['links'].append({
                            'link': url,
                            'title': 'Link %s' % item['resolution'],
                            'type': item['resolution'],
                            'resolve': True
                        })
                    else:
                        movie['links'].append({
                            'link': self.get_hls_playlist(url),
                            'title': 'Link hls',
                            'type': 'hls',
                            'resolve': False
                        })
            elif jsonresponse['embedUrls']:
                for item in jsonresponse['embedUrls']:
                    url = CryptoAES().decrypt(item, bytes(self.key.encode('utf-8')))
                    if not re.search('hydrax', url):
                        movie['links'].append({
                            'link': url,
                            'title': 'Link Unknow',
                            'type': 'Unknow',
                            'resolve': False
                        })
                    else:
                        movie['links'].append({
                            'link': self.get_hydrax(url),
                            'title': 'Link hls',
                            'type': 'hls',
                            'resolve': True
                        })
        return movie

    def get_server_list(self, servers):
        items = {}
        for server in servers:
            if server.select_one('h3') is not None:
                server_name = server.select_one('h3').text.strip().replace("\n", "").encode('utf-8')
            else:
                return None

            if server_name not in items: items[server_name] = []

            if len(server.select('ul.list-episode li a')) > 0:
                for episode in server.select('ul.list-episode li a'):
                    items[server_name].append({
                        'link': episode.get('href'),
                        'title': episode.get('title').encode('utf-8'),
                    })

        return items

    def search_tokenize(self, response):
        m = re.search("eval\(.*\);}\('(.*)','(.*)','(.*)','(.*)'\)\);", response)
        a = self.decode_token(m.group(1), m.group(2), m.group(3), m.group(4))
        m = re.search("join\(''\);}\('(.*)','(.*)','(.*)','(.*)'\)\);$", a)
        a = self.decode_token(m.group(1), m.group(2), m.group(3), m.group(4))
        m = re.search("join\(''\);}\('(.*)','(.*)','(.*)','(.*)'\)\);$", a)
        a = self.decode_token(m.group(1), m.group(2), m.group(3), m.group(4))
        return a

    def get_decrypt_key(self, response):
        a = self.search_tokenize(response)
        return re.search("setDecryptKey\('(.*)'\);watching", a).group(1)

    def get_token_url(self, response):
        a = self.search_tokenize(response)
        return re.search("'url':'(.*)','method'", a).group(1).replace("ip='+window.CLIENT_IP+'&", "")

    def decode_token(self, w, i, s, e):
        a = 0
        b = 0
        c = 0
        string1 = []
        string2 = []
        string_len = len(w + i + s + e)

        while True:
            if a < 5:
                string2.append(w[a])
            else:
                if a < len(w):
                    string1.append(w[a])
            a += 1
            if b < 5:
                string2.append(i[b])
            else:
                if b < len(i):
                    string1.append(i[b])
            b += 1
            if c < 5:
                string2.append(s[c])
            else:
                if c < len(s):
                    string1.append(s[c])
            c += 1
            if string_len == len(string1) + len(string2) + len(e):
                break

        raw_string1 = ''.join(string1)
        raw_string2 = ''.join(string2)
        b = 0
        result = []
        for a in range(0, len(string1), 2):
            ll11 = -1
            if ord(raw_string2[b]) % 2: ll11 = 1
            part = raw_string1[a:a + 2]
            result.append(from_char_code(int(part, 36) - ll11))
            b += 1
            if b >= len(string2):
                b = 0

        return ''.join(result)

    def get_hydrax(self, url):
        response = Request().get(url)
        id = re.search('"key":"(.*?)",', response).group(1)
        params = {
            'key': id,
            'type': 'slug',
            'value': re.search('#slug=(.*)', url).group(1)
        }
        response = Request().post('https://multi.hydrax.net/vip', params, {
            'Origin': 'http://www.phimmoi.net',
            'Referer': 'http://www.phimmoi.net/hydrax.html'
        })

        response = json.loads(response)
        return self.create_hydrax_playlist(url, response)

    def create_hydrax_playlist(self, url, response):
        r = "#EXTM3U\n#EXT-X-VERSION:3\n"
        # if 'origin' in response:
        #     r += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
        #     r += "%s\n" % self.get_hydrax_stream(response['origin'])
        # if 'fullhd' in response:
        #     r += "#EXT-X-STREAM-INF:BANDWIDTH=2998000,RESOLUTION=1920x1080\n"
        #     r += "%s\n" % self.get_hydrax_stream(response['fullhd'])
        if 'hd' in response:
            r += "#EXT-X-STREAM-INF:BANDWIDTH=1998000,RESOLUTION=1280x720\n"
            r += "%s\n" % self.get_hydrax_stream(response['hd'])
        # if 'mhd' in response:
        #     r += "#EXT-X-STREAM-INF:BANDWIDTH=996000,RESOLUTION=640x480\n"
        #     r += "%s\n" % self.get_hydrax_stream(response['mhd'])
        # if 'sd' in response:
        #     r += "#EXT-X-STREAM-INF:BANDWIDTH=394000,RESOLUTION=480x360\n"
        #     r += "%s\n" % self.get_hydrax_stream(response['sd'])

        url = PasteBin().dpaste(r, name=url, expire=60)
        return url

    def get_hydrax_stream(self, stream):
        txt = "#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:" + stream[
            'duration'] + "\n#EXT-X-MEDIA-SEQUENCE:0\n"
        links = []
        if stream['type'] == 2:
            i, j = 0, 0
            for ranges in stream['multiRange']:
                p = 0
                for xrange in ranges:
                    txt += "#EXTINF:%s,\n" % stream['extinf'][i]
                    txt += "#EXT-X-BYTERANGE:%s\n" % xrange
                    g, y = xrange.split('@')
                    g = int(g)
                    y = int(y)
                    f = i > 0 and p + 1 or y
                    p = y and f + g - 1 or g - 1
                    part = '%s-%s.js' % (f, p)

                    url = "%s/%s/%s/%s/%s/%s" % (
                        'http://immortal.hydrax.net',
                        stream['id'],
                        stream['range'][j],
                        stream['expired'],
                        stream['multiData'][j]['file'],
                        part
                    )

                    links.append(url)
                    txt += "%s\n" % url
                    i += 1
                j += 1

        txt += "#EXT-X-ENDLIST\n"

        arequest = AsyncRequest()
        results = arequest.head(links, headers={
            'origin': 'http://www.phimmoi.net'
        })
        for i in range(len(links)):
            try:
                txt.replace(links[i], results[i].headers['location'])
            except:
                print(links[i])
                # print(results[i].headers)

        url = PasteBin().dpaste(txt, name=stream['id'], expire=60)
        return url

    def get_hls_playlist(self, url):
        r = "#EXTM3U\n#EXT-X-VERSION:3\n"
        r += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
        r += "%s\n" % self.get_hls_playlist_stream(url)

        url = PasteBin().dpaste(r, name=url, expire=60)
        return url

    def get_hls_playlist_stream(self, url):
        req = Request()
        response = req.get(url)

        links = re.findall('(https?://(?!so-trym).*)\r', response)
        if links:
            arequest = AsyncRequest(request=req)
            results = arequest.head(links, headers={
                'origin': 'http://www.phimmoi.net',
                'referer': self.originURL
            }, redirect=False)

            for i in range(len(links)):
                response = response.replace(links[i], results[i].headers['location'])

        links = re.findall('(http://so-trym.*)\r', response)
        if links:
            for i in range(len(links)):
                url = '%s|referer=%s' % (links[i], self.originURL)
                response = response.replace(links[i], url)

        url = PasteBin().dpaste(response, name=url, expire=60)
        return url
