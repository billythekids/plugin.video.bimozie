# coding: utf8
from bs4 import BeautifulSoup
import re


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
        for server in servers[-1:]:
            items = server.select('> span.ipsDataItem_main > p')
            for item in items:
                link = self.get_link(item)
                if link: movie['links'].append(link)

        return movie

    def get_link(self, item):
        try:
            link = item.select_one('a').get('href')
            return {
                'link': link,
                'title': item.getText().strip().encode('utf-8')
            }
        except: pass
