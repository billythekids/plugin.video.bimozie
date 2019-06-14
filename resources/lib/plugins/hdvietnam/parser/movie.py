# coding=utf-8
from bs4 import BeautifulSoup
import re
import utils.xbmc_helper as helper


class Parser:

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

    def get(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        posts = soup.select("ol.messageList > li.message > div.messageInfo > div.messageContent > article > blockquote")
        for post in posts:
            self.extract_links(post, movie['links'])

        return movie

    def extract_links(self, content, lists):
        allow_url = ['fshare.vn']
        for link in content.select('a.externalLink'):
            url = link.get('href')
            if True in map(lambda x: x in url, allow_url):
                lists.append({
                    'link': url,
                    'title': link.text.encode('utf-8'),
                    'type': 'Unknown',
                    'resolve': False
                })
