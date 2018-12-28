# coding: utf8
from bs4 import BeautifulSoup
import re
import json
from aes import CryptoAES
from mozie_request import Request


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    key = "phimbathu.com4590481877"

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")

        episodes = soup.select('div.list-episode > a')
        if skipEps is False and len(episodes) > 0:
            for episode in episodes:
                movie['episode'].append({
                    'link': episode.get('href'),
                    'title': ("Tap %s" % episode.text).encode('utf-8')
                })
        else:
            return self.get_link(response)

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # get all server list
        # soup = BeautifulSoup(response, "html.parser")
        # servers = soup.select("div.list-server > div.server-item")
        # for server in servers:
        #     server_name = server.select_one('div.name span').find(text=True, recursive=False).strip().encode('utf-8')
        #     if server_name not in movie['group']: movie['group'][server_name] = []
        #     for ep in server.select('div.option > span'):
        #         movie['group'][server_name].append({
        #             'link': ep.get('data-index'),
        #             'title': ep.get('title').encode('utf-8'),
        #         })

        json_path = re.search("var playerSetting = ({.*});", response.decode('utf-8'))
        print("***********************Get Movie Link*****************************")
        json_response = json.loads(json_path.group(1))
        self.key += json_response['modelId']

        movies = []
        for path in json_response["sourceLinks"]:
            media = path['links'][0]
            url = CryptoAES().decrypt(media["file"], bytes(self.key.encode('utf-8')))
            if not self.check_link(movies, url):
                if media['label'].encode('utf-8') == 'SD':
                    continue
                movie_type = int(media['label'][0:-1])
                label = media['label'].encode('utf-8')
                if media['type'].encode('utf-8') == 'links':
                    url, movie_type, label = self.parse_link(url)
                    if not url: continue
                else: continue
                movies.append({
                    'link': url,
                    'type': movie_type,
                    'title': label
                })

        movie['links'] = sorted(movies, key=lambda elem: elem['type'], reverse=True)[0:1]
        return movie

    def check_link(self, item_list, link):
        for item in item_list:
            if item['link'] == link:
                return True
        return False

    def parse_link(self, url):
        try:
            response = Request().get(url)
            data = json.loads(response)
            movies = sorted(data, key=lambda elem: elem['label'][0:-1], reverse=True)
            return movies[0]['file'], int(movies[0]['label'][0:-1]), movies[0]['label'].encode('utf-8')
        except:
            return (None,None,None)
