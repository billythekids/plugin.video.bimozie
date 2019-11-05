from urllib import urlencode


def get_link(url, media):
    header = {
        'Referrer': media.get('originUrl'),
        'Origin': 'http://biphim.tv',
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36"
    }
    return url + "|%s" % urlencode(header)

