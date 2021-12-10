# -*- coding: utf-8 -*-

import re

from .. import xbmc_helper as helper
from ..mozie_request import Request


def get_link(url):
    helper.log("*********************** Apply archive.org url %s" % url)
    req = Request()

    response = req.get(url, redirect=True)
    m = re.search('property="twitter:player:stream".*content="(.*?)"', response)
    if m:
        url = m.group(1)

    return url, 'archive'
