from utils.mozie_request import Request
from phim7z.parser.category import Parser as Category
from phim7z.parser.channel import Parser as Channel
from phim7z.parser.movie import Parser as Movie
import urllib, re


class Phim7z:
    domain = "https://phim7z.tv"
    api = "https://player.phim7z.tv/hls/getlink.php?id=%s"

    def __init__(self):
        self.request = Request()

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:

            url = '%s%s/page/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, url):
        response = self.request.get(url)
        mid = re.search(r'id:\s"(\d+)",', response).group(1)
        # https://phim7z.tv/ajax/get_episodes/10567
        response = self.request.get("%s/ajax/get_episodes/%s" % (self.domain, mid))
        return Movie().get(response)

    def getLink(self, movie):
        # https://phim7z.tv/ajax/get_sources/130447
        response = self.request.get("%s/ajax/get_sources/%s" % (self.domain, movie['link']))
        return Movie().get_link(response, self.request, self.api, self.domain)

    def search(self, text, page=1):
        url = "%s/search/%s/" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response)
