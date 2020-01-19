from urlparse import urlparse
from urllib import urlencode


def get_link(url, media, including_agent=True):
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc

    print "Apply CORS url %s" % media.get('originUrl')

    header = {
        'Referer': media.get('originUrl'),
        'Origin': base_url
    }

    if including_agent:
        header['User-Agent'] = "Chrome/59.0.3071.115 Safari/537.36"
    return url + "|%s" % urlencode(header), base_url
