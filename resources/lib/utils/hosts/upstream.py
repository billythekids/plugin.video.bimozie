# -*- coding: utf-8 -*-
import re

from .. import xbmc_helper as helper
from ..mozie_request import Request
from .. import cpacker as Packer


def get_link(url):
    response = Request().get(url)
    sources = re.search(r'(eval\(function\(p,a,c,k,e,d\).*)', response)
    if sources:
        sources = Packer.unpack(sources.group(1))
        print(sources)
        sources = re.search(r'sources:\s?(\[.*?\]),', sources)
        if sources:
            sources = helper.convert_js_2_json(sources.group(1))
            url = sources[0].get('file')
            url = url.replace(',.urlset/master', '/index-v1-a1')
            url = url.replace(',', '')

    # https://s96.upstreamcdn.co/hls/w47ryeoxw5bnx2nro2b26rfykbiep3gad4emlyg3cmafwmhshmscgkkwnnyq/index-v1-a1.m3u8
    # https://s96.upstreamcdn.co/hls/w47ryeoxw5bnx2nro2b26rfykbiep3gad4emlyg3cmafwmhshmsickswnnyq/index-v1-a1.m3u8

    return url, 'upstream'
