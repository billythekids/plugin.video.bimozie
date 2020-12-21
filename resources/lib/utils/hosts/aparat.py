# -*- coding: utf-8 -*-
import re, json
from utils.mozie_request import Request
import utils.xbmc_helper as helper


def get_link(url):
    print "*********************** Apply Apparat url %s" % url
    response = Request().get(url)
    sources = re.search(r'sources:\s(\[.*\]),', response)
    if sources:
        sources = helper.convert_js_2_json(sources.group(1))
        url = sources[0].get('src')

    return url, 'aparat'
