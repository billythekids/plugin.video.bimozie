import re, json, base64
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode


def get_link(url, movie):
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    if url.endswith('m3u8'):
        header = {
            'Origin': 'http://www.vtv16.com',
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Referrer': movie.get('originUrl')
        }
        return url + "|%s" % urlencode(header), 'hls3'

    # method 1
    try:
        mid = re.search(r'\?id=(.*)', url).group(1)
        hosturl = '%s/getHost/%s' % (base_url, mid)
        response = Request().post(hosturl, headers={
            'origin': base_url,
            'referer': url
        })

        movie_url = base64.b64decode(response)

        header = {
            'Origin': 'http://www.vtv16.com',
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Referrer': movie.get('originUrl')
        }
        return movie_url + "|%s" % urlencode(header), 'hls3'
    except:
        pass

    # method 2
    request = Request()
    request.get(url)

    location = request.get_request().history[0].headers['Location']
    base_url = urlparse(location)
    base_url = base_url.scheme + '://' + base_url.netloc

    # https://vip4.movie3s.net/public/dist/index.html?id=0676953662683db3977a8d30e4084414
    mid = re.search(r'\?id=(.*)', location).group(1)

    return '%s/hls/%s/%s.playlist.m3u8' % (base_url, mid, mid), 'hls5'

    # method 3
    medias = json.loads(request.post('%s/vl/%s' % (base_url, mid)))

    if '720p' in medias:
        return create_stream(medias['720p'], base_url)

    return url, 'hls5'


def create_stream(stream, base_url):
    txt = "#EXTM3U\n#EXT-X-VERSION:5\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:" + str(
        stream['td']) + "\n#EXT-X-MEDIA-SEQUENCE:0\n"

    for i in range(len(stream['data'][0])):
        extif = stream['data'][0][i]
        byterange = stream['data'][1][i]
        chunk = stream['data'][2][i]
        txt += "#EXTINF:%s,\n" % extif
        txt += "#EXT-X-BYTERANGE:%s\n" % byterange
        l, s = byterange.split('@')
        # /drive/hls/8ee495cd1565893812e9b5708ed50d03/8ee495cd1565893812e9b5708ed50d030.html?ch=8ee495cd1565893812e9b5708ed50d03-chunk-0.txt&s=18&l=2431404
        txt += "%s/drive/hls/%s/%s.html?ch=%s-chunk-%s.txt&s=%s&l=%s\n" % \
               (base_url, stream['md5'], stream['md5'], stream['md5'], chunk, s, l)

    txt += "#EXT-X-ENDLIST"

    url = PasteBin().dpaste(txt, name='movie3s', expire=60)
    return url, 'hls5'
