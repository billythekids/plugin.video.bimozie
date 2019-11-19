from urlparse import urlparse
from urllib import urlencode


def get_link(url, media):
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc

    header = {
        'Referer': media.get('originUrl'),
        'Origin': base_url,
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }
    return url + "|%s" % urlencode(header)

