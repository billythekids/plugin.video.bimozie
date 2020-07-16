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

    response = Request().get(url, headers=header)

    source = re.search(r'var\sVIDEO_URL="(.*?)";', response) \
             or re.search(r'var\sVIDEO_URL=swapServer\("(.*)"\);', response)

    if source:
        return cors.get_link(source.group(1), media)

    sources = re.search(r'var\slistFile=(\[.*?\]);', response)
    if sources:
        sources = json.loads(sources.group(1))
        return cors.get_link(sources[0].get('file'), media)

    return None, None
