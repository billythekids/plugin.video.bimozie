#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from utils.mozie_request import Request


def get_link(url):
    response = Request().get(url)
    soup = BeautifulSoup(response, "html.parser")

    sources = soup.select('source')
    for source in sources:
        if source.get('data-res') == '720':
            return source.get('src'), 'mp4'

    return url, 'mp4'
