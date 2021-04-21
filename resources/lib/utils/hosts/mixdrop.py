# -*- coding: utf-8 -*-
# coding=utf-8
import re

from ..cpacker import cPacker as Packer
from ..mozie_request import Request


def get_link(url, media):
    response = Request().get(url)
    enc = re.search(r'(eval\(function\(p,a,c,k,e,d\).*)\s+?', response)

    if enc:
        sources = enc.group(1)
        sources = Packer().unpack(sources)
    else:
        sources = response

    source = re.search(r'wurl="(.*?)";', sources).group(1)
    if 'http' not in source:
        source = 'https:{}'.format(source)

    return source
