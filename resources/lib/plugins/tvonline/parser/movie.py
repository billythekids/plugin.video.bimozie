# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest
from utils.hosts.fshare import FShareVN


class Parser:

    def get(self, response, domain, origin_url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        sources = soup.select('div#severkhac a')

        if len(sources):
            for source in sources:
                movie['links'].append({
                    'link': "{}/{}".format(domain, source.get('name')),
                    'title': source.text,
                    'type': 'live',
                    'resolve': False,
                    'originUrl': origin_url
                })

        return movie

    def get_link(self, item, subtitle):
        link = item.select_one('a')
        if link:
            link = link.get('href')
        return {
            'link': link,
            'title': item.getText().strip().encode('utf-8'),
            'resolve': False,
            'subtitle': subtitle
        }

    def parse_link(self, url):
        return url
