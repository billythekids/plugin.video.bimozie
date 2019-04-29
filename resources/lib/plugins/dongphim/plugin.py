import urllib
from utils.mozie_request import Request
from dongphim.parser.category import Parser as Category
from dongphim.parser.channel import Parser as Channel
from dongphim.parser.movie import Parser as Movie
import utils.xbmc_helper as XbmcHelper


class Dongphim:
    domain = "http://dongphim.net"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s&p=%d' % (self.domain, channel, page-1)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        response = Request().get(id)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/content/search?t=kw&q=%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
