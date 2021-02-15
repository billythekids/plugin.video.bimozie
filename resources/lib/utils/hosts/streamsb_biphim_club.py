# -*- coding: utf-8 -*-
import re, json
from ..mozie_request import Request
import dood


def get_link(url, media):
    response = Request().get(url)
    source = re.search(r'<iframe.*src="(.*?)"', response)
    if source:
        stream_url = dood.get_link(source.group(1), media)
        return stream_url

    return url, 'test'
