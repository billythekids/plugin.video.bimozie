from utils.mozie_request import Request
from xemphimso.parser.category import Parser as Category
from xemphimso.parser.channel import Parser as Channel
from xemphimso.parser.movie import Parser as Movie
import urllib


class Xemphimso:
    domain = "https://xemphimsoz.net"
    api = "https://xemphimsoz.net/api/v1/episodes/%s/player"

    def __init__(self):
        self.request = Request()

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/trang-%d/' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, url):
        response = self.request.get(url)
        url = Movie().get_movie_link(response)
        response = self.request.get(url)
        return Movie().get(response)

    def getLink(self, movie):
        # https://xemphimso.tv/api/v1/episodes/1000289/player
        response = self.request.post(self.api % movie['link'])
        return Movie().get_link(response, self.domain)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s/" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response)
