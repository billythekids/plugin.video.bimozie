# -*- coding: utf-8 -*-
import re, json, base64, xbmcgui, os
import utils.xbmc_helper as helper
from utils.mozie_request import Request
from urlparse import urlparse
from urllib import urlencode


def get_link(url, media):
    request = Request()
    base_url = urlparse(media.get('originUrl'))
    base_url = base_url.scheme + '://' + base_url.netloc
    header = {
        'Referer': url,
        'User-Agent': "Chrome/59.0.3071.115 Safari/537.36",
        'Origin': base_url
    }

    print "Apply iframeembed url %s" % url

    resp = request.get(url, headers=header)
    req = request.get_request()
    if req.history:
        r_url = req.url
        rurl = urlparse(r_url)
        rurl = rurl.scheme + '://' + rurl.netloc
        rid = re.search(r'id=(.*)', r_url).group(1)
        rurl = "{}/getLinkStreamMd5/{}".format(rurl, rid)
        sources = request.get(rurl, headers=header)
        sources = json.loads(sources)
        print 11111111111111111111111111
        print sources
    else:
        sources = re.search(r'sources\s?[=:]\s?(\[.*?\])', resp, re.DOTALL)
        if sources:
            sources = "".join([s for s in sources.group(1).splitlines() if s.strip("\r\n")])
            sources = re.sub(r'\s+', '', sources)
            sources = helper.convert_js_2_json(sources)
            print 2222222222222222222222222
        print sources

    if sources:
        if len(sources) > 1:
            listitems = []
            for i in sources:
                listitems.append("%s (%s)" % (i.get('label'), i.get('file')))
            index = xbmcgui.Dialog().select("Select stream", listitems)
            if index == -1:
                return None, None
            else:
                return sources[index].get('file') + "|%s" % urlencode(header), sources[index].get('label')
        else:
            return sources[0].get('file') + "|%s" % urlencode(header), sources[0].get('label')

    return None, None
