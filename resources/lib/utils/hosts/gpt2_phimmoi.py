# -*- coding: utf-8 -*-

import json, re
from utils.mozie_request import Request
from urlparse import urlparse
import cors


def get_link(url, media):
    header = {
        'Referer': media.get('originUrl'),
        # 'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        # 'Origin': media.get('originUrl')
    }

    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    id = re.search(r'\/embed\/([a-f0-9]{32})', url).group(1)
    murl = "{}/getLinkStreamMd5/{}".format(base_url, id)
    response = Request().get(murl, headers=header)
    items = json.loads(response)
    items = sorted(items, key=lambda elem: int(elem.get('label')[0:-1]), reverse=True)
    return cors.get_link(items[0].get('file'), media)
