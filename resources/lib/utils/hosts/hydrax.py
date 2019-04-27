import re
import json
import math
import base64
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
import utils.xbmc_helper as helper

origin = "http://www.phimmoi.net"


def get_guest_hydrax(url, media):
    slug = re.search('\?v=(.*)', url).group(1)
    response = Request().post('https://multi.hydrax.net/guest', {
        'slug': slug
    }, {
        'Origin': 'http://hydrax.net'
    })

    response = json.loads(response)
    if 'fullhd' in response:
        return get_hydrax_phimmoi_stream(response['fullhd'], response['servers']), 'hls4'
    elif 'hd' in response:
        return get_hydrax_phimmoi_stream(response['hd'], response['servers']), 'hls4'
    elif 'mhd' in response:
        return get_hydrax_phimmoi_stream(response['mhd'], response['servers']), 'hls4'
    elif 'sd' in response:
        return get_hydrax_phimmoi_stream(response['sd'], response['servers']), 'hls4'
    elif 'origin' in response:
        return get_hydrax_phimmoi_stream(response['origin'], response['servers']), 'hls4'


def get_vip_hydrax(url, media):
    global origin

    response = Request().get(url)
    token = re.search('"key":"(.*?)",', response).group(1)
    params = {
        'key': token,
        'type': 'slug',
        'value': re.search('#slug=(.*)', url).group(1)
    }

    if re.search('vtv16', media['link']):
        origin = "http://live.vtv16.com"

    response = Request().post('https://multi.hydrax.net/vip', params, {
        'Origin': origin
    })

    response = json.loads(response)
    r = "#EXTM3U\n#EXT-X-VERSION:3\n"
    if 'fullhd' in response:
        return get_hydrax_phimmoi_stream(response['fullhd'], response['servers']), 'hls4'
        # r += "#EXT-X-STREAM-INF:BANDWIDTH=2998000,RESOLUTION=1920x1080\n"
        # r += "%s\n" % get_hydrax_phimmoi_stream(response['fullhd'], response['servers'])
    elif 'hd' in response:
        return get_hydrax_phimmoi_stream(response['hd'], response['servers']), 'hls4'
        # r += "#EXT-X-STREAM-INF:BANDWIDTH=1998000,RESOLUTION=1280x720\n"
        # r += "%s\n" % get_hydrax_phimmoi_stream(response['hd'], response['servers'])
    elif 'mhd' in response:
        return get_hydrax_phimmoi_stream(response['mhd'], response['servers']), 'hls4'
        # r += "#EXT-X-STREAM-INF:BANDWIDTH=996000,RESOLUTION=640x480\n"
        # r += "%s\n" % get_hydrax_phimmoi_stream(response['mhd'], response['servers'])
    elif 'sd' in response:
        return get_hydrax_phimmoi_stream(response['sd'], response['servers']), 'hls4'
        # r += "#EXT-X-STREAM-INF:BANDWIDTH=394000,RESOLUTION=480x360\n"
        # r += "%s\n" % get_hydrax_phimmoi_stream(response['sd'], response['servers'])
    elif 'origin' in response:
        return get_hydrax_phimmoi_stream(response['origin'], response['servers']), 'hls4'
        # r += "#EXT-X-STREAM-INF:BANDWIDTH=3998000,RESOLUTION=9999x9999\n"
        # r += "%s\n" % get_hydrax_phimmoi_stream(response['origin'], response['servers'])

    url = PasteBin().dpaste(r, name=url, expire=60)
    return url, 'hls4'


def get_hydrax_phimmoi_stream(stream, n):
    global origin

    txt = "#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:" + stream[
        'duration'] + "\n#EXT-X-MEDIA-SEQUENCE:0\n"

    if 'hash' in stream:
        txt += "#EXT-X-HASH:%s\n" % stream['hash']
        txt += "#EXT-X-KEY:METHOD=AES-128,URI=\"%s\",IV=%s\n" % (stream['hash'], stream['iv'])

    links = []

    r = len(stream['range'])
    o = len(n)
    a = 'expired' in stream and stream['expired'] or None
    s = 0
    l = stream['multiRange']
    h = len(l)

    if stream['type'] == 2:
        r = 0
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
                # c += stream['id'] and "/" + stream['id'] + "/" + stream['range'][t] or ""
                if '@' in l[t][d]:
                    if l[t][d].find('@') == -1: continue
                    g, y = l[t][d].split('@')
                    g, y = int(g), int(y)
                    f = d and p + 1 or y
                    p = y and f + g - 1 or g - 1
                    y = '%s-%s' % (f, p)

                if a:
                    url = a and c + "/" + a + "/" + u
                else:
                    url = c + "/" + str(r) + "/" + str(u)
                # url += stream['id'] and "/" + y + ".js" or "/" + y + ".jpg"
                if url not in links:
                    links.append(url)

                txt += url + "\n"
                r += 1
            if h == t + 1:
                txt += "#EXT-X-ENDLIST"

    elif stream['type'] == 3:
        for t in range(h):
            u = stream['multiData'][t]['file']
            if s < o:
                c = n[s]
                s += 1
            else:
                s = 1
                c = n[0]

            txt += "#EXTINF:" + stream['extinf'][t] + ",\n"
            c = "http://" + c
            # e.id && (c = c + "/" + e.id)
            c += stream['id'] and "/" + stream['id'] or ""
            url = a and c + "/basic/" + a + "/" + u + "." + (
                    stream['id'] and "js" or "jpg") or c + "/basic/" + r + "/" + u + "." + (
                          stream['id'] and "js" or "jpg")

            if url not in links:
                links.append(url)

            txt += url + "\n"
            r += 1
            if h == t + 1:
                txt += "#EXT-X-ENDLIST"

    arequest = AsyncRequest()

    results = arequest.get(links, headers={
        'origin': origin
    })

    media_urls = []
    for i in range(len(links)):
        try:
            media_url = json.loads(results[i])['url']
            txt = txt.replace(links[i], media_url)
            if media_url not in media_urls:
                media_urls.append(media_url)
        except:
            print(links[i])

    if stream['type'] == 2:
        max_targetduration = 12
        play_list = "#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:12\n#EXT-X-MEDIA-SEQUENCE:0\n"
        if 'hash' in stream:
            path = helper.write_file('hydrax.m3u8', stream['hash'].encode(), binary=True)
            path = path.replace('\\', '/')
            # url = PasteBin().dpaste(stream['hash'], name='hydrax.key', expire=60)
            play_list += "#EXT-X-KEY:METHOD=AES-128,URI=\"file://%s\",IV=%s\n" % (path, stream['iv'])

        for link in media_urls:
            slashlink = link.replace('-', '\\-')
            slashlink = slashlink.replace('*', '\\*')
            slashlink = slashlink.replace('?', '\\?')
            segments = re.findall(
                r"(#EXTINF:([0-9]*\.?[0-9]+),\n#EXT-X-BYTERANGE:([0-9]+)@([0-9]+)(?:(?!#EXTINF).)*" + slashlink + ")",
                txt, re.DOTALL)
            duration = 0
            lengthbyte = 0
            startbyte = 999999999
            for segment in segments:
                duration += float(segment[1])
                startbyte = int(segment[3]) < startbyte and int(segment[3]) or startbyte
                lengthbyte += int(segment[2])

            play_list += "#EXTINF:%s,\n" % duration
            play_list += "#EXT-X-BYTERANGE:%s@%s\n" % (lengthbyte, startbyte)
            play_list += "%s\n" % link
            if duration > max_targetduration:
                max_targetduration = duration

        play_list = play_list.replace("TARGETDURATION:12", "TARGETDURATION:" + str(int(math.ceil(max_targetduration))))
        play_list += "#EXT-X-ENDLIST"
    elif stream['type'] == 3:
        play_list = txt

    url = PasteBin().dpaste(play_list, name=stream['id'], expire=60)
    return url
