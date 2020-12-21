# -*- coding: utf-8 -*-
import re, json
from utils.mozie_request import Request
import utils.xbmc_helper as helper
from urllib import urlencode
import cors


def get_link(url, media):
    print "*********************** Apply xemtivimienphi url %s" % url
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66",
        'referer': media.get('originUrl')
    }
    response = Request().get(url, headers=header)
    source = re.search(r'source:\s?"(.*?)",', response)
    if source:
        url = source.group(1)
    sources = re.search(r'sources:\s?(\[.*?\])', response)

    if sources:
        url = helper.convert_js_2_json(sources.group(1))[0]

    source = re.search(r"video.src\s?=\s'(.*?)'", response)
    if source:
        url = source.group(1)

    return url, 'OnlineTv'
