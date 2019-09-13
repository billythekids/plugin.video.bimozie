from urllib import urlencode


def get_link(url, movie):
    # url += '|referer=' + urllib.quote_plus(movie.get('referer'))
    header = {
        'Origin': movie.get('originUrl'),
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Referrer': movie.get('originUrl')
    }
    return url + "|%s" % urlencode(header), 'hls'
