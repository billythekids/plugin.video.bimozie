# coding=utf-8
import re
import json
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.findAll('link', {'rel': 'next'})[0].get('href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.list-server > div.server")
        for server in servers:
            server_name = server.select_one('h3.server-name').getText().strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.list-episode > li > a'):
                movie['group'][server_name].append({
                    'link': ep.get('href').encode('utf-8'),
                    'title': 'Episode %s' % ep.text.strip().encode('utf-8'),
                })

        return movie

    def get_link(self, response, domain, movie_url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select("div#ploption > a.btn-sv")

        jobs = [{'url': '%s%s' % (domain, i.get('data-href')), 'parser': Parser.extract_link} for i in servers]
        group_links = AsyncRequest().get(jobs)

        for links in group_links:
            for link in links:
                movie['links'].append({
                    'link': link[0],
                    'title': 'Link %s' % link[1],
                    'type': link[1],
                    'originUrl': movie_url,
                    'resolve': False
                })

        return movie

    @staticmethod
    def extract_link(response, args=None):
        links = []
        m = re.search(r"sources:\s?(\[.*?\])", response)

        if m is not None:
            sources = m.group(1)
            valid_json = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', sources)
            valid_json = valid_json.replace(',]', ']')
            sources = json.loads(valid_json)

            if len(sources) > 0:
                for s in sources:
                    source = (s['file'], s['label'].encode('utf-8'))
                    links.append(source)
        else:
            source = re.search(r"<iframe.*src=\"(.*?)\"", response)
            if source:
                source = (source.group(1), 'hls')
                links.append(source)

        return links
