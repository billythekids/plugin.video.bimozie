import re
from urlparse import urlparse
from urllib import urlencode


def get_link(url, movie):
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    mid = re.search(r'\?id=((?:(?!\?).)*)', url).group(1)

    header = {
        'Origin': 'http://dongphim.net'
    }

    url = "%s/hls/%s/%s.playlist.m3u8" % (base_url, mid, mid)

    return url + "|%s" % urlencode(header), 'hls3'
