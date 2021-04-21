# -*- coding: utf-8 -*-
import re

from ..link_extractor import LinkExtractor
from ..mozie_request import Request

from . import cors


def get_link(url, media):
    req = Request()
    response = req.get(url)

    match = re.search(r'''<div id="player">(.*?)</div>''', response)
    if match:
        url = LinkExtractor.iframe(match.group(1))
        response = req.get(url, headers={
            'referer': 'https://thuckhuya.com'
        })

    match = re.search(r'''var urlStream = "(.*?)"''', response)
    if match:
        url = match.group(1)

    return cors.get_link(url, media)
