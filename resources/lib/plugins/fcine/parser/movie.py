# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest
from utils.hosts.fshare import FShareVN
from kodi_six.utils import py2_encode


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
        items = server.select('span.ipsDataItem_main a')

        links = []
        for link in items:
            f_url = 'https://www.fshare.vn/api/v3/files/folder?linkcode=%s' % FShareVN.extract_code(link.get('href'))
            if link and 'fshare' in link.get('href'): links.append(f_url)

        if len(links) > 0:
            results = AsyncRequest().get(links)
            for idx, result in enumerate(results):
                try:
                    link = items[idx].get('href')
                    name, size = FShareVN.get_asset_info(content=result)
                    movie['links'].append({
                        'link': link,
                        'title': '[%s] %s' % (size, name),
                        'type': 'Fshare',
                        'isFolder': FShareVN.is_folder(link),
                        'subtitle': subtitle,
                        'resolve': False
                    })
                except:
                    print('Link die %s' % items[idx].get('href'))
                    continue

        return movie

    def get_link(self, item, subtitle):
        link = item.select_one('a')
        if link:
            link = link.get('href')
        return {
            'link': link,
            'title': py2_encode(item.getText().strip()),
            'resolve': False,
            'subtitle': subtitle
        }

    def parse_link(self, url):
        return url
