# -*- coding: utf-8 -*-
import re

from ..mozie_request import Request

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from .. import xbmc_helper as helper


def get_link(url, media):
    helper.log("*********************** Apply tvmienphi url %s" % url)
    header = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': media.get('originUrl')
    }

    req = Request()

    response = req.get(url, headers=header)
    url_path = re.search(r'''play\('(.*?)'\)''', response).group(1)
    if 'http' not in url_path:
        local = urlparse(url)
        url_path = "{}://{}{}".format(local.scheme, local.hostname, url_path)

    url = req.get(url_path, headers=header)
    helper.log(url)

    return url + "|%s" % urlencode(header), 'tvmienphi'
