import urllib
from mozie_request import Request
from tvhay.parser.category import Parser as Category
from tvhay.parser.channel import Parser as Channel
from tvhay.parser.movie import Parser as Movie


class Tvhay:
    domain = "http://tvhay.org/"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/page/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(Request().get(id))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, url):
        response = Request().get(url)
        return Movie().get_link(response)

    def search(self, text):
        url = "%ssearch/%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
