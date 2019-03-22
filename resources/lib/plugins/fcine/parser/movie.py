# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


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
            subtitle = servers[-2:-1][0].select_one('span.ipsDataItem_main > a').get('href')
        except:
            pass

        server = servers[-1:][0]
        items = server.select('> span.ipsDataItem_main > p')
        for item in items:
            link = self.get_link(item, subtitle)
            if link:
                movie['links'].append(link)

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
