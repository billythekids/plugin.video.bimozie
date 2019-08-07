#!/usr/bin/env python
# coding=utf-8
import re, json
from utils.mozie_request import Request
from utils.cpacker import cPacker as Packer


def get_link(url):
    response = Request().get(url)
    enc = re.search(r'(eval\(function\(p,a,c,k,e,d\).*)\s+?', response)

    if enc:
        sources = enc.group(1)
        sources = Packer().unpack(sources)
    else:
        sources = response

    sources = re.search(r'sources:\s?(.*?\]),', sources)
    try:
        sources = re.sub(r'(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources.group(1))
    except: pass

    sources = json.loads(sources)
    for source in sources:
        if 'label' in source and '720' in source['label']:
            return source['file'], 'mp4'

    if len(sources) > 0 and 'file' in sources[0]:
        return sources[0]['file'], 'hls4'

    return url, 'mp4'
