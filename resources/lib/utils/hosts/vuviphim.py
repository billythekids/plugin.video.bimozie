# -*- coding: utf-8 -*-
import re
import json
import urllib
from utils.mozie_request import Request
import utils.xbmc_helper as helper
from utils.cpacker import cPacker as Packer


def get_link(url):
    response = Request().get(url)
    enc = re.search(r'(eval\(function\(p,a,c,k,e,d\).*)\s+?</script>', response)
    enc2 = re.search(r'sources:\s?(\[.*?\]),', response)
    found = False

    print "Apply VUVIPHIM parser"

    if enc:
        sources = enc.group(1)
        sources = Packer().unpack(sources)
        sources = re.search(r'sources:\s?(.*?\]),', sources)
        found = True

    elif enc2:
        sources = enc2.group(1)
        found = True

    if found:
        try:
            sources = re.sub(r'(?<={|,)([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources.group(1))
        except:
            pass
        sources = json.loads(sources)

        print sources
        score = {'sd': 1, 'hd': 2, '360p': 1, '480p': 2, '720p': 3, '1080p': 3}
        if len(sources) > 0:
            try:
                sources = sorted(sources,
                                 key=lambda elem: elem['label'].lower() in score and score[elem['label'].lower()] or 3,
                                 reverse=True)
            except:
                pass

            if len(sources) > 1:
                listitems = ["Link %s (%s)" % (i["label"], i["file"]) for i in sources]
                index = helper.create_select_dialog(listitems)
                if index == -1:
                    return None, 'mp4'
                else:
                    return sources[index]['file'] + '|referer=' + urllib.quote_plus(url), sources[index]['type']
            else:
                return sources[0]['file'] + '|referer=' + urllib.quote_plus(url), sources[0]['type']

    return url, 'vuviphim'
