# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest
from utils.hosts.fshare import FShareVN


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("ul.ipsDataList > div#extraFields > li")

        # get subtitle link
        subtitle = None
        try:
            subtitle = soup.select_one("ul.ipsDataList > div#extraFields > li a.ipsType_success").get('href')
        except:
            pass

        server = servers[-1:][0]
        items = server.select('> span.ipsDataItem_main a')

        links = []
        for link in items:
            if link and 'fshare' in link.get('href'): links.append(link.get('href'))

        if len(links) > 0:
            results = AsyncRequest().get(links)
            for idx, result in enumerate(results):
                try:
                    name, size = FShareVN.get_info(content=result)
                    movie['links'].append({
                        'link': links[idx],
                        'title': '[%s] %s' % (size, name),
                        'type': 'Unknown',
                        'subtitle': subtitle,
                        'resolve': False
                    })
                except:
                    print('Link die %s' % links[idx])
                    continue

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
