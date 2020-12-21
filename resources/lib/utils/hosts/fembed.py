# -*- coding: utf-8 -*-
import re
import json
from utils.mozie_request import Request


def get_link(url):
    print "*********************** Apply fembed url %s" % url

    mid = re.search('/v/(.*)', url).group(1)
    response = Request().post('https://www.fembed.com/api/source/%s' % mid, params={
        'd': 'www.fembed.com', 'r': ''
    })
    response = json.loads(response)
    response = response['data']
    sources = sorted(response, key=lambda elem: int(elem['label'][0:-1]), reverse=True)

    return sources[0]['file'], sources[0]['label']
