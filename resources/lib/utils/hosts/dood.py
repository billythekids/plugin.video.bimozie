# -*- coding: utf-8 -*-
import random
import re
import string
import time
from cloudscraper2 import CloudScraper
from .. import xbmc_helper as helper
from ..mozie_request import Request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def get_link(url, movie):
    helper.log("*********************** Apply dood url %s" % url)
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    scraper = CloudScraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'windows',
        'mobile': False
    }, allow_brotli=False)

    response = scraper.get(url).text
    match = re.search(r'''\$.get\('(/pass_md5/.*?)',''', response)
    # print(response)
    token = re.search(r'''return a\+"(.*?)"''', response, re.MULTILINE).group(1)
    if match:
        header = {
            'Referer': url
        }
        # token = match.group(2)
        m_url = base_url + match.group(1)
        response = scraper.get(m_url, headers=header)
        return dood_decode(response.text) + token + str(int(time.time() * 1000)) + "|%s" % urlencode(header), 'dood'

    return url, 'dood'


def dood_decode(data):
    t = string.ascii_letters + string.digits
    return data + ''.join([random.choice(t) for _ in range(10)])
