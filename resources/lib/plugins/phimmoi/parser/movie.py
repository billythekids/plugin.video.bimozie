# -*- coding: utf-8 -*-
import re

import utils.xbmc_helper as helper
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from utils.link_extractor import LinkExtractor

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_playlink(self, response, url):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('a#btn-film-watch').get('href')

    def get(self, response, url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        self.originURL = url

        try:
            error = py2_encode(
                soup.select_one('div.error-not-available div.alert-subheading').find(text=True, recursive=False))
            if error:
                helper.message(error, 'Not Found')
                return movie
        except:
            pass

        # get episode if possible
        servers = soup.select('div.list-server > div.server.clearfix')
        if skipEps is False and len(servers) > 0:
            helper.log("***********************Get Movie Episode*****************************")
            found = False
            items = self.get_server_list(servers)
            if items is not None and len(items) > 0:
                movie['group'] = items
                found = True
            else:
                found = False
            if found is False:
                servers = soup.select('ul.server-list > li.backup-server')
                movie['group'] = self.get_server_list(servers)

        else:
            movie['group']['phimmoi'] = [{
                'link': self.originURL,
                'title': 'Unknown link'
            }]

        return movie

    def get_link(self, response, url, request, domain):
        helper.log("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        filmid = re.search(r'filmID\s?=\s?parseInt\((\d+)\);', response).group(1)
        epid = re.search(r'episodeID\s?=\s?parseInt\((\d+)\);', response).group(1)
        svid = re.search(r'svID\s?=\s?parseInt\((\d+)\);', response).group(1)

        ajax_url = '{}/ajax/player'.format(domain)
        resp = request.post(ajax_url, params={
            'id': filmid,
            'ep': epid,
            'sv': svid,
        })

        frame_url = urlparse(LinkExtractor.iframe(resp))

        movie_url = parse_qs(frame_url.query).get('url')[0]
        movie['links'].append({
            'link': movie_url,
            'title': 'Link {}'.format('HD'),
            'type': 'hls',
            'resolve': False,
            'originUrl': url
        })

        return movie

    def get_server_list(self, servers):
        items = {}
        for server in servers:
            if server.select_one('h3') is not None:
                server_name = py2_encode(server.select_one('h3').text.strip().replace("\n", ""))
            else:
                return None

            if server_name not in items: items[server_name] = []

            if len(server.select('ul.list-episode li a')) > 0:
                for episode in server.select('ul.list-episode li a'):
                    items[server_name].append({
                        'link': episode.get('href'),
                        'title': py2_encode(episode.get('title'))
                    })

        return items
