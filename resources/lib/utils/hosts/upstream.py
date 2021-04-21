# -*- coding: utf-8 -*-
import re

from .. import xbmc_helper as helper
from ..mozie_request import Request


def get_link(url):
    response = Request().get(url)
    sources = re.search(r'sources:\s(\[.*\]),', response)
    if sources:
        sources = helper.convert_js_2_json(sources.group(1))
        url = sources[0].get('file')

    return url, 'upstream'
