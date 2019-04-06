import re
import json
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin


def get_link(url):
    response = Request().get(url)
    token = re.search('"key":"(.*?)",', response).group(1)
    params = {
        'key': token,
        'type': 'slug',
        'value': re.search('#slug=(.*)', url).group(1)
    }
    response = Request().post('https://multi.hydrax.net/vip', params, {
        'Origin': 'http://www.phimmoi.net',
        'Referer': 'http://www.phimmoi.net/hydrax.html'
    })

    response = json.loads(response)
    r = "#EXTM3U\n#EXT-X-VERSION:3\n"
    if 'hd' in response:
        return get_hydrax_phimmoi_stream(response['hd'], response['servers']), 'hls4'
        r += "#EXT-X-STREAM-INF:BANDWIDTH=1998000,RESOLUTION=1280x720\n"
        r += "%s\n" % get_hydrax_phimmoi_stream(response['hd'], response['servers'])
    elif 'fullhd' in response:
        r += "#EXT-X-STREAM-INF:BANDWIDTH=2998000,RESOLUTION=1920x1080\n"
        r += "%s\n" % get_hydrax_phimmoi_stream(response['fullhd'], response['servers'])
    elif 'mhd' in response:
        r += "#EXT-X-STREAM-INF:BANDWIDTH=996000,RESOLUTION=640x480\n"
        r += "%s\n" % get_hydrax_phimmoi_stream(response['mhd'], response['servers'])
    elif 'sd' in response:
        r += "#EXT-X-STREAM-INF:BANDWIDTH=394000,RESOLUTION=480x360\n"
        r += "%s\n" % get_hydrax_phimmoi_stream(response['sd'], response['servers'])
    elif 'origin' in response:
        r += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
        r += "%s\n" % get_hydrax_phimmoi_stream(response['origin'], response['servers'])

    url = PasteBin().dpaste(r, name=url, expire=60)
    # url = "%s|origin=%s" % (url, 'http://www.phimmoi.net')
    return url, 'hls4'


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

                c = "http://" + c
                c += stream['id'] and "/" + stream['id'] + "/" + stream['range'][t] or ""
                if '@' in l[t][d]:
                    if l[t][d].find('@') == -1: continue
                    g, y = l[t][d].split('@')
                    g, y = int(g), int(y)
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

    # arequest = AsyncRequest()
    # results = arequest.head(links, headers={
    #     'origin': 'http://www.phimmoi.net'
    # })
    #
    #
    # media_urls = list()
    # for i in range(len(links)):
    #     try:
    #         media_url = results[i].headers['location']
    #         txt = txt.replace(links[i], media_url)
    #         media_urls.append(media_url)
    #     except:
    #         print(links[i])

    url = PasteBin().dpaste(txt, name=stream['id'], expire=60)
    url = "%s|origin=%s" % (url, 'http://www.phimmoi.net')
    return url
