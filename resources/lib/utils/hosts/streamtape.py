# -*- coding: utf-8 -*-
import re
from utils.mozie_request import Request


def get_link(url, media):
    response = Request().get(url)
    # <div id="videolink" style="display:none;">//streamtape.com/get_video?id=jAVyPBzZ6RTa69&expires=1591773984&ip=F0EsD0ISKxSHDN&token=9zFuzldNBybP</div>
    match = re.search(r'id="videolink".*?>(.*?)</div>', response)
    print(match)
    if match:
        print(match.group(1))
        return match.group(1), 'streamtape'

    return None, None
