# -*- coding: utf-8 -*-

import json
import re

import xbmcgui
from six.moves.html_parser import HTMLParser
from ..mozie_request import Request


def rsl(s):
    s = str(s).replace('HDG', '') \
        .replace('HD', '1080') \
        .replace('SD', '480') \
        .replace('sd', '480') \
        .replace('large', '640') \
        .replace('lowest', '240') \
        .replace('low', '360') \
        .replace('hd', '720') \
        .replace('full', '1080') \
        .replace('Auto', '640') \
        .replace('medium', '240') \
        .replace('mobile', '144') \
        .replace('AUTO', '640')

    result = re.search('(\d+)', s)
    if result:
        return result.group(1)
    else:
        return '240'


def get_link(url):
    if 'apitvh.net' in url \
            or 'tvhayz.net' in url \
            or 'tvhays.org' in url \
            or 'tvhai.org' in url \
            :
        url = re.search(r'\?link=(.*)', url).group(1)

    response = Request().get(url)
    m = re.search('data-options="(.+?)"', response)
    h = HTMLParser()
    try:
        s = m.group(1)
    except:
        raise Exception("Link has been removed")
    s = h.unescape(s)
    s = json.loads(s)
    s = json.loads(s['flashvars']['metadata'])
    items = [(i['url'], rsl(i['name'])) for i in s['videos']]
    items = sorted(items, key=lambda elem: int(elem[1]), reverse=True)

    if len(items) == 1:
        return items[0]

    listitems = []
    for i in items:
        listitems.append("%s (%s)" % (i[1], i[0]))
    index = xbmcgui.Dialog().select("Select ok.ru stream", listitems)
    if index == -1:
        return None, None
    else:
        return items[index]
