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
        else:
            print("***********************Get Movie Link*****************************")
            sources = re.findall("file: (.*), label: \"(\d+)\"", response, re.MULTILINE)
            sources = sorted(sources, key=lambda elem: elem[1], reverse=True)
            for source in sources:
                # test2 = define18("aHR0cHM6Ly9iaXQubHkvMnpFN0ttZz90ZXN0PXUwMDAwaHR0cHM6Ly9iaXQubHkvMnpFN0ttZz90ZXN0PQ==")
                match = re.search(source[0]+"=.*\(\"(.*)\"\)", response)
                if match is not None:
                    link = self.decode(match.group(1))
                    movie['links'].append({
                        'link': link,
                        'title': 'Link %sp' % source[1],
                        'type': source[1]
                    })
                    if source[1] >= 720: break
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

        r = r.replace("ms.com/51.mp4/", "https://3.bp.blogspot.com/")
        r = r.replace("ms.com/52.mp4/", "https://video.xx.fbcdn.net/")
        r = r.replace("ms.com/53.mp4/", "v/t42.9040-2/")
        r = r.replace("ms.com/54.mp4/", "https://lh3.googleusercontent.com/")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("ms.com/55.mp4/", "=m37")
        r = r.replace("ms.com/56.mp4/", "=m22")
        r = r.replace("ms.com/57.mp4/", "=m18")

        r = r.replace("amazon.com/61.mp4/", "https://3.bp.blogspot.com/")
        r = r.replace("amazon.com/62.mp4/", "https://video.xx.fbcdn.net/")
        r = r.replace("amazon.com/63.mp4/", "v/t42.9040-2/")
        r = r.replace("amazon.com/64.mp4/", "https://lh3.googleusercontent.com/")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("https://bit.ly/2zE7Kmg?test=", "")
        r = r.replace("amazon.com/65.mp4/", "=m37")
        r = r.replace("amazon.com/66.mp4/", "=m22")
        r = r.replace("amazon.com/67.mp4/", "=m18")
        return r
