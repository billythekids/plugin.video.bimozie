# -*- coding: utf-8 -*-

import json, re
from utils.mozie_request import Request
import cors


def get_link(url, media):
    header = {
        'Referer': media.get('originUrl'),
        # 'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        # 'Origin': media.get('originUrl')
    }

    id = re.search(r'\/embed\/([a-f0-9]{32})', url).group(1)
    murl = "https://gpt2.phimmoi.net/getLinkStreamMd5/{}".format(id)
    response = Request().get(murl, headers=header)
    items = json.loads(response)
    items = sorted(items, key=lambda elem: int(elem.get('label')[0:-1]), reverse=True)
    return cors.get_link(items[0].get('file'), media)
