#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from ..mozie_request import Request


def get_link(url):
    response = Request().get(url)
    soup = BeautifulSoup(response, "html.parser")

    source = soup.select_one('#videolink').text.strip()
    url = 'https://verystream.com/gettoken/%s?mime=true' % source

    return url, 'mp4'
