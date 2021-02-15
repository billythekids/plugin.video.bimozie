# -*- coding: utf-8 -*-
import re
from urlparse import urlparse
from urllib import urlencode
from utils.mozie_request import Request
import utils.xbmc_helper as helper


def get_link(url, media):
    print("*********************** Apply Lotus url %s" % url)
    header = {
            'referer': 'https://lotus.vn/',
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        }
    req = Request()
    response = req.get(url, headers=header)
    print(response.encode('utf8'))
    source = re.search(r'"link":\s?"(.*?)",', response)
    
    if '.mp4' in source.group(1):
        url = source.group(1)
        return url, 'lotus'
    if source:
        master_url = source.group(1)
        playlist = get_adaptive_link(Request().get(master_url, headers=header))
        listitems = []
        for i in playlist:
            listitems.append("%s (%s)" % (i[0], i[1]))

        index = helper.create_select_dialog(listitems)
        if index == -1:
            return None, None
        else:
            url = playlist[index][1]
            url = "{}|{}".format(url, urlencode(header))

    return url, 'lotus'


def get_adaptive_link(response):
    resolutions = re.findall(r'RESOLUTION=\d+x(\d+)', response)
    matches = re.findall(r'^(?!#)(.{8,})', response, re.MULTILINE)
    playlist = []
    #
    if '240' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if 240 == int(i)), -1)
        url = matches[idx]
        playlist.append([240, url])
    if '360' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if 360 == int(i)), -1)
        url = matches[idx]
        playlist.append([360, url])
    if '480' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if 480 == int(i)), -1)
        url = matches[idx]
        playlist.append([480, url])
    if '720' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if 720 == int(i)), -1)
        url = matches[idx]
        playlist.append([720, url])
    if '1080' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if 1080 == int(i)), -1)
        url = matches[idx]
        playlist.append([1080, url])

    return playlist
