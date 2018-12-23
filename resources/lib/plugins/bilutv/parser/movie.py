# coding: utf8
from bs4 import BeautifulSoup
import re
import json
from aes import CryptoAES
from mozie_request import Request


class Parser:
    key = "bilutv.net4590481877"

    def get(self, response, skipEps=False):
        movie = {
            'links': [],
            'episode': [],
            'group': []
        }
        soup = BeautifulSoup(response, "html.parser")

        # get episode if posible
        episodes = soup.select('ul.list-episode > li')
        if skipEps is False and len(episodes) > 0:
            for episode in episodes:
                movie['episode'].append({
                    'link': episode.select_one('a').get('href'),
                    'title': "Tap %s" % episode.select_one('a').text
                })
        else:
            json_path = re.search("var playerSetting = ({.*});", response.decode('utf-8'))
            print("***********************Get Movie Link*****************************")
            json_response = json.loads(json_path.group(1))
            self.key += json_response['modelId']

            if self.find_tm_link(response, soup, movie['links']) is False:
                for path in json_response["sourceLinks"]:
                    link = path['links'][0]
                    url = CryptoAES().decrypt(link["file"], bytes(self.key.encode('utf-8')))
                    if link['type'] == "links":
                        # fetch_links.append(url)
                        # movie['links'] += self.get_link(url, path['label'])
                        links = self.get_link(url, path['label'])
                        if len(links) > 0:
                            movie['links'] = links
                            break

            print(movie)

        return movie

    def get_link(self, url, label):
        links = []
        response = Request().get(url)
        jsonresponse = json.loads(response.decode('utf-8'))

        for link in jsonresponse:
            if link['type'] == "video/mp4" and self.checkLink(links, link) is False and link['label'] != "360p" and \
                    link['label'] != "480p":
                links.append({
                    'link': link['file'],
                    'title': "[%s] %s" % (link['label'].encode("utf-8"), label.encode("utf-8")),
                    'type': link['type'].encode("utf-8")
                })
        return links

    def checkLink(self, list, link):
        for item in list:
            if 'file' in link:
                if item['link'] == link['file']:
                    return True
            else:
                if item['link'] == link['link']:
                    return True
        return False

    def find_tm_link(self, response, soup, links):
        found = False
        score = {'dr': 0, 'sb': 3, 'cs': 2, 'st': 5, 'ls': 4, 'db': 3, 'op': 7, 'sm': 8, 'gd': 9, 'yt': 10, 'gs': 11,
                 'gp': 12, 'ga': 12, 'dl': 12}
        # getJSON("/ajax/getLinkPlayer/id/87360/index/"+index
        link_id = re.search("\"/ajax/getLinkPlayer/id/(\d+)/index/\"", response).group(1)
        link_list = []

        for server in soup.select('div.server-item'):
            type = server.select_one("div.name span").text.strip()
            found = True
            items = []
            for link in server.select("div.option span"):
                items.append((link.get('title'), link.get('data-index'), score[link.get('title')]))
            items.sort(key=comparator, reverse=True)
            link_list += self.get_link_player(link_id, items, type)

        if len(link_list) > 0:
            links += link_list
        else:
            return False
        return found

    def get_link_player(self, id, tuple_servers, label):
        links = []
        items = []
        # for server in tuple_servers:
        #     response = Request().get("http://bilutv.net/ajax/getLinkPlayer/id/%s/index/%s" % (id, server[1]))
        #     jsonresponse = json.loads(response)
        #     for path in jsonresponse['sourceLinks']:
        #         link = path['links'][0]
        #         url = CryptoAES().decrypt(link["file"], bytes(self.key.encode('utf-8')))
        #         items.append(url)
        server = tuple_servers[0]
        response = Request().get("http://bilutv.net/ajax/getLinkPlayer/id/%s/index/%s" % (id, server[1]))
        jsonresponse = json.loads(response)
        for path in jsonresponse['sourceLinks']:
            link = path['links'][0]
            url = CryptoAES().decrypt(link["file"], bytes(self.key.encode('utf-8')))
            items.append(url)

        if len(items) > 0:
            items = list(set(items))
            for url in items:
                if re.search('getcs', url):
                    print("*********************** Get link server: %s type: " % (server[1]), label)
                    found_links = self.get_link(url, label)
                    for item in found_links:
                        if self.checkLink(links, item) is False:
                            links += found_links
                    print("*********************** End link server: %s type: " % (server[1]), label)
                    if len(links) > 0:
                        return links

        return links


def comparator(a):
    return a[2]
