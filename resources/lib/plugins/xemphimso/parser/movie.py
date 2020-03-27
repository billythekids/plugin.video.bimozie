# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json
from utils.aes import CryptoAES


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("div.movie_info > div.movie-poster > div.wrap-btn > a.btn-danger").get('href')

    def get(self, response):
        movie = {
            'links': [],
            'episode': [],
            'group': {}
        }
        soup = BeautifulSoup(response, "html.parser")

        servers = soup.select('div#xpo-list-server > div.htmlwrap')
        for server in servers:
            server_name = server.select_one(
                'div.xpo-server > div.col-md-3 > span.xpo-server-name').getText().strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('div.xpo-server > div.col-md-9 > ul.xpo-list-eps > li > a'):
                movie['group'][server_name].append({
                    'link': ep.get('data-id').encode('utf-8'),
                    'title': 'Episode %s' % ep.select_one('span').text.strip().encode('utf-8'),
                })

        return movie

    def get_link(self, response, domain):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        response = re.search(r'"source":({.*?}})', response)
        if response:
            response = json.loads(response.group(1), encoding='utf-8')
            if len(response['medias']['levels']) > 0:
                for file in response['medias']['levels']:
                    url = CryptoAES().decrypt(file['file'], file['key'])
                    movie['links'].append({
                        'link': url,
                        'title': 'Link %s' % file['label'],
                        'type': file['type'],
                        'resolve': False,
                        'originUrl': domain
                    })
                    print

        return movie
