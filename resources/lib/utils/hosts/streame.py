# -*- coding: utf-8 -*-

from ..mozie_request import Request
import re
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def get_link(url, media):
    header = {
        # 'referer': media.get('originUrl'),
        'referer': 'https://dongphymtv.com/',
        'origin': 'https://dongphymtv.com/',
        'user-agent':  "Chrome/59.0.3071.115 Safari/537.36"
    }

    if '/v1' in url:
        response = Request().get(url, headers=header)
        # name="streamid" content="e08c28d1-38fc-4e30-bd3f-0503d162c52f"
        m = re.search(r'''name="streamid"\s?content="(.*?)"''', response)
        if m:
            url = 'https://streame.cloud/v1/video/manifest/{}/|{}'.format(m.group(1), urlencode({
                'user-agent':  "Chrome/59.0.3071.115 Safari/537.36"
            }))

    return url, 'streame'
