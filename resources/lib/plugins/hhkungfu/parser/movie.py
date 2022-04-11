# coding=utf-8
import re
import json
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest
from kodi_six.utils import py2_encode


def from_char_code(*args):
    return ''.join(map(chr, args))

class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.findAll('a', {'class': 'btn btn-sm btn-danger watch-movie visible-xs-blockx'})[0].get('href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        servers = soup.select("div#halim-list-server.list-eps-ajax")
        for server in servers:
            server_name = py2_encode(server.select_one('a').getText().strip())
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul.halim-list-eps > li > a'):
                movie['group'][server_name].append({
                    'link': py2_encode(ep.get('href')),
                    'title': 'Tập %s' % py2_encode(ep.text.strip()),
                })
        return movie

    def get_link(self, response, domain, movie_url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        div = soup.find("div", class_="clearfix wrap-content")
        scr = str(div.find("script"))
        data = json.loads(re.findall(r'halim_cfg[^{]+(.*)</script>', str(scr), flags=re.DOTALL)[0])
        EPI = data['episode_slug']
        PID = data['post_id']
        SVID = data['server']
        servers = soup.select("div#halim-ajax-list-server > span")
        jobs = [{'url': f"{domain}/wp-content/themes/halimmovies/player.php?episode_slug={EPI}&server_id={SVID}&subsv_id={i.get('data-subsv-id')}&post_id={PID}&nonce=&custom_var=", 'parser': Parser.extract_link} for i in servers]
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Safari/537.36',
            'Accept': 'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }        
        group_links = AsyncRequest().get(jobs,headers = h)
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
        jData = json.loads(response)
        source = re.search(r"<iframe.*src=\"(.*?)\"", jData['data']['sources'])        
        ytb = re.search(r"youtube", response)
        if ytb:
            source = ( f'https:{source.group(1)}' , 'NICE')
        else:
            source = (source.group(1), 'NICE')
        links.append(source)
        return links
