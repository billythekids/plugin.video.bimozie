# -*- coding: utf-8 -*-

import re, json, xbmc
from bs4 import BeautifulSoup
from utils.aes import CryptoAES
from utils.mozie_request import AsyncRequest


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one("div.movie_info > div.movie-poster > div.wrap-btn > a.btn-danger").get('href')

    def get(self, response, originURL):
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
                    'link': "{}|{}".format(originURL, ep.get('data-id').encode('utf-8')),
                    'title': 'Episode %s' % ep.select_one('span').text.strip().encode('utf-8'),
                })

        return movie

    def get_link(self, response, domain, request, originURL):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        self.originURL = originURL
        response = re.search(r'"source":(\[.*?\])', response)
        if response:
            response = json.loads(response.group(1), encoding='utf-8')
            if len(response) > 0:
                jobs = []
                for file in response:
                    if 'HDX' not in file['namesv']:
                        url = CryptoAES().decrypt(file['link'], file['key'])
                        if 'stream' in file['typeplay']:
                            jobs.append({'url': url, 'parser': Parser.extract_link})
                        else:
                            movie['links'].append({
                                'link': url,
                                'title': 'Link %s' % file['namesv'],
                                'type': file['namesv'],
                                'resolve': False,
                                'originUrl': originURL
                            })

                for job in jobs:
                    try:
                        Parser.extract_link(request.get(job.get('url'), headers={
                            # 'origin': domain,
                            'referer': originURL
                        }), (movie['links'], originURL))
                        xbmc.sleep(1000)
                    except: pass

                # AsyncRequest(request=request, retry=1, thread=1).get(jobs, headers={
                #     'origin': 'https://xomphimhay.com',
                # 'referer': originURL
                # }, args=(movie['links'], originURL))
        return movie

    @staticmethod
    def extract_link(response, args):
        response = json.loads(response, encoding='utf-8')
        movie_links, originURL = args
        if len(response) > 0:
            for m in response:
                url = CryptoAES().decrypt(m['file'], m['key'])
                if 'http://' in url or 'https://' in url:
                    item = {
                        'link': url,
                        'title': 'Link %s' % m['label'],
                        'type': m['type'],
                        'resolve': False,
                        'originUrl': originURL
                    }
                    movie_links.append(item)
        else:
            raise Exception("Error")
