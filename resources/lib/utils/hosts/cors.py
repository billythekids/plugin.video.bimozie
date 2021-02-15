# -*- coding: utf-8 -*-
import re
from urlparse import urlparse
from urllib import urlencode
from utils.mozie_request import Request


def get_link(url, media, including_agent=True):
    print "Apply CORS url %s" % media.get('originUrl')
    if media.get('originUrl'):
        base_url = urlparse(media.get('originUrl'))
        base_url = base_url.scheme + '://' + base_url.netloc
        host_url = urlparse(url)

        header = {
            'Referer': media.get('originUrl'),
            'Origin': base_url,
            'verifypeer': 'false'
        }

        if including_agent:
            header['User-Agent'] = "Chrome/59.0.3071.115 Safari/537.36"

        if 'vdicdn.com' in url:
            # url = url.replace('vdicdn.com', '8giaitri.com')
            # host_url = urlparse(url)
            header = {
                # 'Referer': 'https://phim1080.me',
                # 'Referer': media.get('originUrl'),
                # 'Host': host_url.netloc,
                # 'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            }

            url = get_adaptive_link(Request().get(url, headers=header))
            url = host_url.scheme + '://' + host_url.netloc + url
            # print "--------------------------- {}".format(url)
            return url + "|%s" % urlencode(header), host_url.netloc

        return url + "|%s" % urlencode(header), "CORS"
    return url, 'CORS'


def get_adaptive_link(response):
    resolutions = re.findall(r'RESOLUTION=\d+x(\d+)', response)
    matches = re.findall(r'^(?!#)(.*)', response, re.MULTILINE)
    if '720' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
        url = matches[idx]
    # if '1080' in resolutions:
    #     idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
    #     url = matches[idx]
    # elif '720' in resolutions:
    #     idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
    #     url = matches[idx]
    # elif '480' in resolutions:
    #     idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
    #     url = matches[idx]
    # elif '360' in resolutions:
    #     idx = next((resolutions.index(i) for i in resolutions if '360' == i), -1)
    #     url = matches[idx]
    # if '//' in url[0:2]:
    #     url = "{}{}".format("https:", url)

    return url
