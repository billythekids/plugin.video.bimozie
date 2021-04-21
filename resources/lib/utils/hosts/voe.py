# -*- coding: utf-8 -*-
import re

from ..mozie_request import Request


def get_link(url):
    response = Request().get(url)
    source = re.search(r'<source src="(.*?)"', response)
    if source:
        url = source.group(1)

    return url, 'voe.sx'
