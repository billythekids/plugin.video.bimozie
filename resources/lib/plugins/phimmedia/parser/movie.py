# coding: utf8
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
        if skipEps is False and len(episodes) > 0:
            for episode in episodes:
                for ep in episode.select('div.page-tap > ul > li > a'):
                    server = episode.select_one('h4').text.strip().encode('utf-8')
                    if server not in movie['group']: movie['group'][server] = []
                    movie['group'][server].append({
                        'link': ep.get('href').encode('utf-8'),
                        'title': ep.get('title').encode('utf-8'),
                    })
                    # movie['episode'].append({
                    #     'link': ep.get('href'),
                    #     'title': ep.get('title').encode('utf-8'),
                    # })
        else:
            print("***********************Get Movie Link*****************************")
            # test2 = define18("aHR0cHM6Ly9iaXQubHkvMnpFN0ttZz90ZXN0PXUwMDAwaHR0cHM6Ly9iaXQubHkvMnpFN0ttZz90ZXN0PQ==");
            matches = re.findall("test\d=define18\(\"(.*)\"\);", response)
            matches = list(set(matches))
            if matches is not None:
                for idx, m in enumerate(matches):
                    link = self.decode(m)
                    if len(link) > 20 or re.findall('(u0000)', link) is None:
                        movie['links'].append({
                            'link': link,
                            'title': 'Link %d' % idx,
                            'type': idx
                        })
        return movie

    def decode(self, link):
        r = base64.b64decode(link)
        r = r.replace("bbc.com/51.mp4/", "https://3.bp.blogspot.com/")
        r = r.replace("bbc.com/52.mp4/", "https://video.xx.fbcdn.net/")
        r = r.replace("bbc.com/53.mp4/", "v/t42.9040-2/")
        r = r.replace("bbc.com/54.mp4/", "https://lh3.googleusercontent.com/")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("bbc.com/55.mp4/", "=m37")
        r = r.replace("bbc.com/56.mp4/", "=m22")
        r = r.replace("bbc.com/57.mp4/", "=m18")
        return r
