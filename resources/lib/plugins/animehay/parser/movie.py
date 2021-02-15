# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.mozie_request import AsyncRequest
from utils.pastebin import PasteBin
from urlparse import urlparse
import utils.xbmc_helper as helper
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('div#ah-pif > div.ah-pif-head > div.ah-pif-ftool > div.ah-float-left > span > a').get(
            'href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.ah-wf-body > div.ah-wf-le")
        for server in servers:
            server_name = server.select_one('div.ah-le-server > span').text.strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul > li > a'):
                movie['group'][server_name].append({
                    'link': ep.get('href').encode('utf-8'),
                    'title': 'Episode %s' % ep.text.encode('utf-8'),
                })

        return movie

    def get_link(self, response, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.findall(r"<iframe.*?src=['|\"](http.*?)['|\"]\s?", response)
        if len(sources) > 0:
            for source in sources:
                if source in 'http://lb.animehay.tv/play/' and len(source) == len('http://lb.animehay.tv/play/'):
                    continue

                movie['links'].append({
                    'link': source,
                    'title': 'Link direct',
                    'type': 'mp4',
                    'resolve': False
                })

        sources = re.search(r'player.setup.*"sources":\s?(\[.*?\])', response, re.DOTALL)

        if sources:
            sources = json.loads(sources.group(1))
            if sources and len(sources) > 0:
                for source in sources:
                    movie['links'].append({
                        'link': source['file'],
                        'title': 'Link %s' % source['label'],
                        'type': source['type'],
                        'resolve': False
                    })

        sources = re.search(r"<iframe.*?src=['|\"](.*animehay.tv/play/{5,}.*?)['|\"]\s?", response)
        if sources:
            res = Request()
            if 'key=' in sources.group(1):
                vkey = re.search('key=(.*)', sources.group(1)).group(1)
                # http://vl.animehay.tv/initPlayer/f555b31844becd2e378d4978457014521af38ab8e66834ade1062b44827ef642
                resp = res.post('http://vl.animehay.tv/initPlayer/%s' % vkey)
                resp = json.loads(resp)
                if 'availablePlayers' not in resp:
                    return movie

                if 'p2pdrive' in resp['availablePlayers']:
                    data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('p2pdrive', vkey)))
                    source = data['data']

                    if source:
                        movie['links'].append({
                            'link': source,
                            'title': 'Link p2pdrive',
                            'type': 'hls',
                            'resolve': False
                        })

                if 'gphoto' in resp['availablePlayers']:
                    data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('gphoto', vkey)))
                    data = res.get(data['data'])
                    sources = json.loads(re.search(r"var\s?sources\s?=\s?(\[.*?\])", data).group(1))
                    if sources and len(sources) > 0:
                        for source in sources:
                            movie['links'].append({
                                'link': source['file'],
                                'title': 'Link %s' % source['label'],
                                'type': 'mp4',
                                'resolve': False
                            })

                if 'fembed' in resp['availablePlayers']:
                    data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('fembed', vkey)))
                    data = res.get(data['data'])
                    source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)
                    if source:
                        movie['links'].append({
                            'link': source,
                            'title': 'Link fembed',
                            'type': 'mp4',
                            'resolve': False
                        })

                if 'okru' in resp['availablePlayers']:
                    data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('okru', vkey)))
                    data = res.get(data['data'])
                    source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)
                    if source:
                        movie['links'].append({
                            'link': source,
                            'title': 'Link okru',
                            'type': 'mp4',
                            'resolve': False
                        })

                if 'openload' in resp['availablePlayers']:
                    data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('openload', vkey)))
                    data = res.get(data['data'])
                    source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)
                    if source:
                        movie['links'].append({
                            'link': source,
                            'title': 'Link openload',
                            'type': 'mp4',
                            'resolve': False
                        })
                return movie
            else:
                res.get(sources.group(1))
                link = res.get_request().url
                vkey = re.search('id=(.*)', link)
                if vkey:
                    vkey = vkey.group(1)
                    base_url = urlparse(link)
                    base_url = base_url.scheme + '://' + base_url.netloc
                    urlVideo = "{}/hls/{}/{}.playlist.m3u8".format(base_url, vkey, vkey)

                    movie['links'].append({
                        'link': urlVideo,
                        'title': 'Link p2pdrive',
                        'type': 'hls',
                        'resolve': False,
                        'originUrl': originUrl
                    })

        sources = re.search(r'player.setup\((.*?)\);', response, re.DOTALL)
        if sources:
            source = sources.group(1)
            source = re.search(r'"file":\s"(.*?)",', source)
            movie['links'].append({
                'link': source.group(1),
                'title': 'Link direct',
                'type': 'mp4',
                'resolve': False
            })

        sources = re.search(r"var\s?source\s?=\s?(\[.*?\]);", response)
        if sources:
            sources = helper.convert_js_2_json(sources.group(1))
            for source in sources:
                movie['links'].append({
                    'link': source.get('file'),
                    'title': 'Link %s' % source.get('label').encode('utf-8'),
                    'type': source.get('type').encode('utf-8'),
                    'originUrl': originUrl,
                    'resolve': False
                })

        sources = re.search(r'var\s?source\s?=\s?"(\[.*?\])";', response)
        if sources:
            sources = helper.convert_js_2_json(sources.group(1).replace('\\', ''))
            for source in sources:
                movie['links'].append({
                    'link': source.get('file'),
                    'title': 'Link %s' % source.get('label').encode('utf-8'),
                    'type': source.get('type').encode('utf-8'),
                    'originUrl': originUrl,
                    'resolve': False
                })
        # sources = re.search('<script rel="nofollow" src="(.*)" async>', response)
        # if sources:
        #     response = Request().get(sources.group(1))
        #     if 'links:' in response:
        #         sources = json.loads(re.search('links: (.*?),', response).group(1))
        #         for key, value in sources.items():
        #             if value:
        #                 label = key[1:].encode('utf-8')
        #                 movie['links'].append({
        #                     'link': value,
        #                     'title': 'Link %s' % label,
        #                     'type': label,
        #                     'resolve': True
        #                 })
        #
        #         movie['links'] = sorted(movie['links'], key=lambda elem: int(elem['type']), reverse=True)

        return movie
