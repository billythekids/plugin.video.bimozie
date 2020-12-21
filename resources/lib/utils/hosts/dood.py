# -*- coding: utf-8 -*-
import re, string, random, time
from utils.mozie_request import Request
from urllib import urlencode


def get_link(url, movie):
    print "*********************** Apply dood url %s" % url
    req = Request()
    response = req.get(url)
    match = re.search(r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''', response, re.DOTALL)
    if match:
        header = {
            'Referer': url
        }
        token = match.group(2)
        url = 'https://dood.to' + match.group(1)
        response = req.get(url, headers=header)
        return dood_decode(response) + token + str(int(time.time() * 1000)) + "|%s" % urlencode(header), 'dood'

    return url, 'dood'


def dood_decode(data):
    t = string.ascii_letters + string.digits
    return data + ''.join([random.choice(t) for _ in range(10)])
