# coding=utf-8
from bs4 import BeautifulSoup
import re
import utils.xbmc_helper as helper
from utils.mozie_request import AsyncRequest
from utils.hosts.fshare import FShareVN


class Parser:
    found_links = []

    def is_block(self, response):
        block = False
        postLinks = []
        soup = BeautifulSoup(response, "html.parser")
        b = r'color:red;padding: 10px;font-weight: bold;font-size: 14px;border: 1px solid #f9d9b0'
        posts = soup.select("ol.messageList > li.message > div.messageInfo")
        for post in posts:
            content = post.select_one('div.messageContent > article > blockquote').encode('utf-8')
            if b in content:
                block = True
                postLinks.append(post.select_one('div.messageMeta > div.publicControls > a.LikeLink').get('href'))

        return block, postLinks

    def get(self, response, origin_url=""):
        self.found_links = []
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        posts = soup.select("ol.messageList > li.message > div.messageInfo > div.messageContent > article > blockquote")
        for post in posts:
            self.extract_links(post)

        if len(self.found_links) > 0:
            arequest = AsyncRequest()
            results = arequest.get(self.found_links)
            for idx, result in enumerate(results):
                try:
                    name, size = FShareVN.get_info(content=result)
                except:
                    print('Link die %s' % self.found_links[idx])
                    continue

                if name:
                    movie['links'].append({
                        'link': self.found_links[idx],
                        'title': '[%s] %s' % (size, name),
                        'intro': name,
                        'type': 'Unknown',
                        'resolve': False,
                        'isFolder': FShareVN.is_folder(self.found_links[idx]),
                        'originUrl': origin_url
                    })
                else:
                    movie['links'].append({
                        'link': self.found_links[idx],
                        'title': self.found_links[idx],
                        'type': 'Unknown',
                        'resolve': False,
                        'isFolder': FShareVN.is_folder(self.found_links[idx]),
                        'originUrl': origin_url
                    })

        return movie

    def extract_links(self, content):
        allow_url = ['fshare.vn/']

        for link in content.select('a.externalLink'):
            url = link.get('href')
            if True in map(lambda x: x in url, allow_url) and url not in self.found_links:
                self.found_links.append(url)
