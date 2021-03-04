# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from utils.link_extractor import LinkExtractor
from utils.mozie_request import Request
from six.moves.urllib.parse import parse_qsl, urlencode, urlparse


class Parser:

    def get(self, response, domain, origin_url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # get all server list
        url = LinkExtractor.iframe(response)
        response = Request().get(url)
        soup = BeautifulSoup(response, "html.parser")
        sources = soup.select('div.pan > a')
        local = urlparse(url)
        local_path = '/'.join(local.path.split('/')[:-1])

        if len(sources):
            for idx, source in enumerate(sources):
                movie_url = "{}://{}{}/{}".format(local.scheme, local.hostname, local_path, source.get('name'))
                movie['links'].append({
                    'link': movie_url,
                    'title': 'Link %s' % str(idx+1),
                    'type': 'live',
                    'resolve': False,
                    'originUrl': url
                })

        return movie

    def get_link(self, item, subtitle):
        link = item.select_one('a')
        if link:
            link = link.get('href')
        return {
            'link': link,
            'title': py2_encode(item.getText().strip()),
            'resolve': False,
            'subtitle': subtitle
        }

    def parse_link(self, url):
        return url
