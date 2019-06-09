# coding=utf-8
from bs4 import BeautifulSoup
import utils.xbmc_helper as helper
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        return re.search('post_id: (\d+),', response).group(1), \
               re.search('var ajax_player.*"nonce":"(.*)"};', response).group(1)

    def get(self, response, nonce):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.halim-server")
        for server in servers:
            server_name = server.select_one('span.halim-server-name').getText().strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.halim-list-eps > li > span'):
                # postid|serverid|epid|nounce
                id = "%s|%s|%s|%s" % (ep.get('data-post-id'), ep.get('data-server'), ep.get('data-episode'), nonce)
                movie['group'][server_name].append({
                    'link': id,
                    'title': ep.text.strip().encode('utf-8'),
                })

        return movie

    def get_link(self, response, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # subitle
        subtitle = None
        sub_re = re.search(r'tracks:\s?(\[.*\]),', response, re.DOTALL)
        if sub_re:
            try:
                sub_re = re.search(r'file:\s?"(.*?)",', sub_re.group(1))
                subtitle = sub_re.group(1)
            except: pass

        sources = re.search(r'sources:\s?(.*?)\n', response)
        if sources:
            sources = json.loads(sources.group(1).replace('}],', '}]'))
            try:
                sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
            except: pass

            if len(sources) > 0:
                for source in sources:
                    label = 'label' in source and source['label'] or ''
                    movie['links'].append({
                        'link': self.parse_link(source['file']),
                        'title': 'Link %s' % label.encode('utf-8'),
                        'type': label.encode('utf-8'),
                        'resolve': False,
                        'subtitle': subtitle,
                        'originUrl': originUrl
                    })

            return movie

        sources = re.search('<iframe.*src=(".*?")', response)
        if sources is not None:
            source = sources.group(1).replace('"', '')
            if source:
                movie['links'].append({
                    'link': source,
                    'title': 'Link %s' % source.encode('utf-8'),
                    'type': 'Unknow',
                    'resolve': False,
                    'originUrl': originUrl
                })
                return movie

        return movie

    def parse_link(self, url):
        return url
