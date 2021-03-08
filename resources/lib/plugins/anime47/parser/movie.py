# -*- coding: latin1 -*-
import base64
import json
import re
import codecs

import utils.xbmc_helper as helper
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode
from utils.aes import CryptoAES
from utils.link_extractor import LinkExtractor
from utils.mozie_request import AsyncRequest


def text(txt):
    try:
        return txt.encode('latin1').decode('utf-8').strip()
    except:
        return py2_encode(txt, 'latin1').decode('utf-8').strip()


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('a.btn-red').get('href')

    def get(self, response, url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        self.originURL = url

        try:
            error = soup.select_one('div.error-not-available div.alert-subheading').find(text=True,
                                                                                         recursive=False).encode(
                'latin1')
            if error:
                helper.message(error, 'Not Found')
                return movie
        except:
            pass

        # get episode if possible
        servers = soup.select('div.servers > div.server')
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
            movie['group']['anime47'] = [{
                'link': self.originURL,
                'title': 'Unknown link'
            }]

        return movie

    def get_server_list(self, servers):
        items = {}
        for server in servers:
            group_server = server.select('div.name')
            episodes = server.select('div.episodes')
            for i in range(len(group_server)):
                server_name = text(group_server[i].select_one('span').text.strip().replace("\n", ""))
                if server_name not in items: items[server_name] = []
                for episode in episodes[i].select('ul > li > a'):
                    items[server_name].append({
                        'link': episode.get('href'),
                        'title': text(episode.get('data-episode-name'))
                    })

        return items

    def get_link(self, response, domain, originURL, request):
        helper.log("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # get server list
        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select('div#clicksv > span.btn')
        m_id = re.search(r'var id_ep = (.*)', response).group(1)

        jobs = [
            {
                'url': '%s/player/player.php' % domain,
                'parser': Parser.extract_link,
                'params': {
                    'ID': m_id,
                    'SV': i.get('id').replace('sv', '')
                }
            } for i in servers
        ]
        group_links = AsyncRequest(request=request).post(jobs)
        for link in group_links:
            if link:
                movie['links'].append({
                    'link': link,
                    'title': 'Link %s' % 'HD',
                    'type': 'Unknown',
                    'originUrl': originURL,
                    'resolve': False
                })

        return movie

    @staticmethod
    def extract_link(response, args=None):
        url = LinkExtractor.iframe(response)
        if url and 'short.icu' not in url:
            return url
        elif re.search(r'atob\(', response):
            cipher_text = re.search(r'atob\("(.*?)"\)', response).group(1)
            enc_data = json.loads(base64.b64decode(cipher_text))
            # cipher_text = 'Salted__{}{}'.format(
            #     codecs.decode(enc_data['s'], 'hex'),
            #     base64.b64decode(enc_data['ct'])
            # )

            cipher_text = b'Salted__' + bytearray.fromhex(enc_data['s']) + base64.b64decode(enc_data['ct'])
            cipher_text = base64.b64encode(cipher_text)
            url = CryptoAES().decrypt(cipher_text, 'caphedaklak').replace('\\', '').replace('"', '')
            if url:
                return url
        else:
            helper.log(text(response))

        return None
