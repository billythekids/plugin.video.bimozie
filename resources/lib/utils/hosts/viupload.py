# -*- coding: utf-8 -*-

import re

from .. import xbmc_helper as helper
from .. import cpacker
from ..mozie_request import Request


def get_link(url, media):
    helper.log("*********************** Apply viupload.net url %s" % url)
    req = Request()
    response = req.get(url, redirect=True, headers={
        'referer': media.get('originUrl')
    })

    content = cpacker.unpack(response)
    matches = re.findall('''['|"]?file['|"]?:['|"](.*?)['|"]''', content)
    if matches and len(matches) > 0:
        url = matches[0]

    return url, 'viupload'
