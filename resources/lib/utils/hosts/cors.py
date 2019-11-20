from urlparse import urlparse
from urllib import urlencode


def get_link(url, media):
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc

    header = {
        'Referer': media.get('originUrl'),
        'Origin': base_url,
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36"
    }
    return url + "|%s" % urlencode(header)

