# -*- coding: utf-8 -*-
import re, json
from urlparse import urlparse
from urllib import urlencode
from . import cors, hls_parser
from utils.mozie_request import Request
from urlparse import urlparse, parse_qs


def get_link(url, movie):
    print "Apply VProxy parser"
    base_url = urlparse(url)

    mid = parse_qs(base_url.query).get('id')[0]
    base_url = base_url.scheme + '://' + base_url.netloc

    if mid:
        header = {
            'Origin': base_url,
            'Referer': url
        }

        ajax_url = "%s/getlink.php?id=%s" % (base_url, mid)
        response = json.loads(Request().get(ajax_url, headers=header))
        if len(response) > 0:
            m_url = json.loads(response['data'])[0].get('file')
            return cors.get_link(m_url, movie, including_agent=True)

    return None, None

