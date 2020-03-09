# -*- coding: utf-8 -*-
from urllib import urlencode


def get_link(url, media):
    header = {
        'referer': media.get('originUrl'),
        'Origin': 'http://biphim.tv',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    return "{}|{}".format(url, urlencode(header))

