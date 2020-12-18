# -*- coding: latin1 -*-
from bs4 import BeautifulSoup
import re
import json
from utils.aes import CryptoAES


class Parser:
    key = 'motphjm.net45904818772018'

    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("a.btn-see.btn-danger.adspruce-streamlink").get('href')

    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }

        soup = BeautifulSoup(response, "html.parser")
        movie['group']['motphim'] = []
        for ep in soup.select('div.episodes > div.list-episode > a'):
            movie['group']['motphim'].append({
                'link': ep.get('href'),
                'title': '%s' % ep.text.strip().encode('utf8'),
            })

        return movie

    def get_link(self, response, request, api_url, domain, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        datalink = re.search(r'var\sdataLink="(.*)"', response).group(1)
        eid = re.search(r'var\seId="(.*)"', response).group(1)
        vid = re.search(r'var\svId="(.*)"', response).group(1)
        slug = re.search(r'var\sslug="(.*)"', response).group(1)

        # get token
        csrf = re.search(r'<meta name="csrf-token" content="(.*)">', response).group(1)

        response = request.post(api_url, params={
            'x_dataLink': datalink,
            'x_subTitle': '',
            'x_eId': eid,
            'x_vId': vid,
            'x_slug': slug,
        }, headers={
            'Origin': domain,
            'Referer': originUrl
        })

        sources = json.loads(response, encoding='utf8')
        url = CryptoAES().decrypt(sources.get('mirror_link'), self.key)

        movie['links'].append({
            'link': url,
            'title': 'Link motphim',
            'type': 'unknown',
            'resolve': False,
            'originUrl': domain
        })

        return movie
