# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import base64


class Parser:
    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': []
        }
        soup = BeautifulSoup(response, "html.parser")

        # get episode if possible
        episodes = soup.select('div.block-wrapper')
        if len(episodes) > 0:
            for episode in episodes:
                for ep in episode.select('div.page-tap > ul > li > a'):
                    server = episode.select_one('h4').text.strip().encode('utf-8')
                    if server not in movie['group']: movie['group'][server] = []
                    movie['group'][server].append({
                        'link': ep.get('href').encode('utf-8'),
                        'title': ep.get('title').encode('utf-8'),
                    })

        return movie

    def get_link(self, response, url):
        movie = {
            'group': {},
            'episode': [],
            'links': []
        }
        print("***********************Get Movie Link*****************************")
        sources = re.findall("file: (.*), label: \"(\d+)\"", response, re.MULTILINE)
        if sources and len(sources) > 0:
            sources = sorted(sources, key=lambda elem: elem[1], reverse=True)
            for source in sources:
                match = re.search(source[0] + "=.*\(\"(.*)\"\);", response)
                if match is not None:
                    link = self.decode(match.group(1))
                    movie['links'].append({
                        'link': link,
                        'title': 'Link %sp' % source[1],
                        'type': source[1],
                        'resolve': False,
                        'originUrl': url
                    })

            return movie

        sources = re.findall(r'file:\s?[\'|"](.*?)[\'|"],\s?label: "(\d+)"', response, re.MULTILINE)
        if sources and len(sources) > 0:
            for source in sources:
                url = source[0]

                movie['links'].append({
                    'link': url,
                    'title': 'Link %sp' % source[1],
                    'type': source[1],
                    'resolve': False,
                    'originUrl': url
                })

            return movie

    def decode(self, link):
        r = base64.b64decode(link)
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("ms.com?test=", "")

        rep_text = re.findall(r'(?:(?!\d+\.mp4)(.*?/)(\d)(\d).mp4/)', r)
        rep_text = rep_text[0][0] + rep_text[0][1]

        r = r.replace('%s1.mp4/' % rep_text, 'https://3.bp.blogspot.com/')
        r = r.replace('%s2.mp4/' % rep_text, 'https://video.xx.fbcdn.net/')
        r = r.replace('%s3.mp4/' % rep_text, 'v/t42.9040-2/')
        r = r.replace('%s4.mp4/' % rep_text, 'https://lh3.googleusercontent.com/')

        r = r.replace('%s5.mp4/' % rep_text, '=m37')
        r = r.replace('%s6.mp4/' % rep_text, '=m22')
        r = r.replace('%s7.mp4/' % rep_text, '=m18')
        return r
