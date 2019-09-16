import re, json, base64
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin
from urllib import urlencode


def get_link(url, movie):
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    try:
        mid = re.search(r'\?id=(.*)&keyaction', url).group(1)
        hosturl = '%s/hls/%s/%s.playlist.m3u8' % (base_url, mid, mid)

        header = {
            'Origin': base_url,
            'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
            'Referrer': url
        }
        return hosturl + "|%s" % urlencode(header), 'hls5'
    except:
        pass

    return url, 'hls5'
