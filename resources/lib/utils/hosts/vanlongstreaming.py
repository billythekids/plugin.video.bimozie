# -*- coding: utf-8 -*-
import re
import json
from urlparse import urlparse, parse_qs
from urllib import urlencode
import cors


def get_link(url, media):
    print "Apply vanlongstreaming parser"
    base_url = urlparse(url)
    id = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    url = '%s/hls/%s/%s.playlist.m3u8' % (base_url, id, id)
    return cors.get_link(url, media, False)
