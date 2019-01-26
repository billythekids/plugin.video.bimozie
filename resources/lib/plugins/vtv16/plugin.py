import urllib
from utils.mozie_request import Request
from vtv16.parser.category import Parser as Category
from vtv16.parser.channel import Parser as Channel
from vtv16.parser.movie import Parser as Movie


class Vtv16:
    domain = "http://www.vtv16.com"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s?page=%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = '%s/xem-phim.html' % id
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/?s=%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
