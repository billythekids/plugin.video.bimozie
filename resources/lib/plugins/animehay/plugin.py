import urllib
from utils.mozie_request import Request
from animehay.parser.category import Parser as Category
from animehay.parser.channel import Parser as Channel
from animehay.parser.movie import Parser as Movie
import utils.xbmc_helper as XbmcHelper


class Animehay:
    domain = "http://animehay.tv"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s?page=%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(Request().get(id))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/tim-kiem?q=%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
