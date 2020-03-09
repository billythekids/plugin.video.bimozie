# -*- coding: utf-8 -*-
import re
import json
import math
import base64
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
import utils.xbmc_helper as helper
import smamuhh1metro

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
        return get_smamuhh1metro(response['fullhd'], response['ping'], media)
    elif 'hd' in response:
        return get_smamuhh1metro(response['hd'], response['ping'], media)
    elif 'mhd' in response:
        return get_smamuhh1metro(response['mhd'], response['ping'], media)
    elif 'sd' in response:
        return get_smamuhh1metro(response['sd'], response['ping'], media)
    elif 'origin' in response:
        return get_smamuhh1metro(response['origin'], response['ping'], media)


def get_vip_hydrax(url, media):
    global origin

    response = Request().get(url)
    token = re.search(r'"key":"(.*?)",', response).group(1)
    params = {
        'key': token,
        'type': 'slug',
        'value': re.search(r'"value":"(.*?)",', response).group(1)
    }

    if re.search('vtv16', media['link']):
        origin = "http://live.vtv16.com"

    response = Request().post('https://multi.hydrax.net/vip', params, {
        'Origin': origin
    })

    response = json.loads(response)
    if 'fullhd' in response:
        return get_smamuhh1metro(response['fullhd'], response['ping'], media)
    elif 'hd' in response:
        return get_smamuhh1metro(response['hd'], response['ping'], media)
    elif 'mhd' in response:
        return get_smamuhh1metro(response['mhd'], response['ping'], media)
    elif 'sd' in response:
        return get_smamuhh1metro(response['sd'], response['ping'], media)
    elif 'origin' in response:
        return get_smamuhh1metro(response['origin'], response['ping'], media)

    return url


def get_hydrax_phimmoi_stream(stream, n):
    global origin

    txt = "#EXTM3U\n#EXT-X-VERSION:4\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:" + str(stream['duration']) + "\n#EXT-X-MEDIA-SEQUENCE:0\n"

    if 'hash' in stream:
        txt += "#EXT-X-HASH:%s\n" % stream['hash']
        txt += "#EXT-X-KEY:METHOD=AES-128,URI=\"%s\",IV=%s\n" % (stream['hash'], stream['iv'])
        # helper.message('Encrypt not supported', 'Hydrax')
        # return ""

    links = []
    hashlist = []

    r = s = 0
    a = 'expired' in stream and stream['expired'] or None

    if stream['type'] == 2:
        o = len(n)
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
                    # find has
                    match = re.search(r"immortal.hydrax.net/\d+/(.*?)$", url)
                    if match and match.group(1) not in hashlist:
                        links.append(url)
                        hashlist.append(match.group(1))
                    elif not match:
                        links.append(url)

                txt += url + "\n"
                r += 1
            if h == t + 1:
                txt += "#EXT-X-ENDLIST"

    elif stream['type'] == 3:
        d = stream['ranges']
        l = len(d)
        o = stream['expired']
        a = s = 0
        u = stream['datas']
        for t in range(l):
            f = u[t]['file']
            for p in range(len(d[t])):
                if a < r:
                    c = n[a]
                    a += 1
                else:
                    a = 1
                    c = n[0]
                    y = d[t][p]
                    c = "http://" + c

                    txt += "#EXTINF:%s,\n" % stream['extinfs'][s]
                    txt += "#EXT-X-BYTERANGE:%s\n" % y
                    if o:
                        url = c + "/" + o + "/" + f + "/" + y
                    else:
                        url = c + "/" + s + "/" + f + "/" + y

                    txt += "%s\n" % url
                    s += 1
            if l == t + 1:
                txt += "#EXT-X-ENDLIST"

        # for t in range(l):
        #     u = stream['datas'][t]['file']
        #     if s < o:
        #         c = n[s]
        #         s += 1
        #     else:
        #         s = 1
        #         c = n[0]
        #
        #     txt += "#EXTINF:" + stream['extinfs'][t] + ",\n"
        #     c = "http://" + c
        #     # e.id && (c = c + "/" + e.id)
        #     c += stream['id'] and "/" + stream['id'] or ""
        #     url = a and c + "/basic/" + a + "/" + u + "." + (
        #             stream['id'] and "js" or "jpg") or c + "/basic/" + r + "/" + u + "." + (
        #                   stream['id'] and "js" or "jpg")
        #
        #     if url not in links:
        #         links.append(url)
        #
        #     txt += url + "\n"
        #     r += 1
        #     if h == t + 1:
        #         txt += "#EXT-X-ENDLIST"

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
        play_list = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-TARGETDURATION:12\n#EXT-X-MEDIA-SEQUENCE:0\n"
        if 'hash' in stream:
            # path = helper.write_file('hydrax.m3u8', stream['hash'], binary=True)
            # path = path.replace('\\', '/')
            # path = "http://localhost/portal/hydrax.m3u8"
            path = "encrypted-file://" + stream['hash']
            # url = PasteBin().dpaste(stream['hash'], name='hydrax.key', expire=60)
            play_list += "#EXT-X-KEY:METHOD=AES-128,URI=\"%s\",IV=%s\n" % (path, stream['iv'])

        for index, link in enumerate(media_urls):
            if len(hashlist) > 0:
                slashlink = hashlist[index]
            else:
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

    url = PasteBin().dpaste(play_list, name='hydrax', expire=60)
    return url


def get_smamuhh1metro(stream, server, media):
    if 'smamuhh1metro' in server:
        url = "%s/%s/0/playlist.m3u8" % (server, stream.get('sig'))
        return smamuhh1metro.get_link(url, media)
