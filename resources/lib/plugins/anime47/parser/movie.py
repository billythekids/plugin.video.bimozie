# -*- coding: latin1 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request, AsyncRequest
import utils.xbmc_helper as helper
from utils.link_extractor import LinkExtractor
import re
import json
import base64
from utils.aes import CryptoAES


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
            print("***********************Get Movie Episode*****************************")
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
                server_name = group_server[i].select_one('span').text.strip().replace("\n", "").encode('latin1')
                if server_name not in items: items[server_name] = []
                for episode in episodes[i].select('ul > li > a'):
                    items[server_name].append({
                        'link': episode.get('href'),
                        'title': episode.get('data-episode-name').encode('latin1')
                    })

        return items



        for server in servers:
            if server.select_one('div.name > span') is not None:
                server_name = server.select_one('div.name > span').text.strip().replace("\n", "").encode('latin1')
            else:
                return None

            if server_name not in items: items[server_name] = []

            if len(server.select('ul > li > a')) > 0:
                for episode in server.select('ul > li > a'):
                    items[server_name].append({
                        'link': episode.get('href'),
                        'title': episode.get('data-episode-name').encode('latin1')
                    })

        return items

    def get_link(self, response, domain, originURL, request):
        print("***********************Get Movie Link*****************************")
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
            cipher_text = 'Salted__' + enc_data['s'].decode('hex') + base64.b64decode(enc_data['ct'])
            cipher_text = base64.b64encode(cipher_text)
            url = CryptoAES().decrypt(cipher_text, 'caphedaklak').replace('\\', '').replace('"', '')
            if url:
                return url
        else:
            print response.encode('latin1')

        return None
