# -*- coding: utf-8 -*-
import json

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs
from utils.mozie_request import Request

from . import cors
import utils.xbmc_helper as helper


def get_link(url, movie):
    helper.log("Apply VProxy parser")
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

