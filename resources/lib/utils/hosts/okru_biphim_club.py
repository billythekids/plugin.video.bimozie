# -*- coding: utf-8 -*-
import json
import re

from ..mozie_request import Request

from . import ok


def get_link(url, media):
    response = Request().get(url)
    sources = re.search(r'var array = (\[.*\]);', response)
    if sources:
        sources = json.loads(sources.group(1))
        url = sources[0]

    return ok.get_link(url)
