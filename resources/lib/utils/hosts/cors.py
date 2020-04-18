# -*- coding: utf-8 -*-

from urlparse import urlparse
from urllib import urlencode


def get_link(url, media, including_agent=True):
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc
    host_url = urlparse(url)

    if media.get('originUrl'):
        print "Apply CORS url %s" % media.get('originUrl')

        header = {
            'Referer': media.get('originUrl'),
            'Origin': base_url,
            'verifypeer': 'false'
        }

        if including_agent:
            header['User-Agent'] = "Chrome/59.0.3071.115 Safari/537.36"

        return url + "|%s" % urlencode(header), host_url.netloc
    return url, host_url.netloc
