from mozie_request import Request
from bilutv.parser.category import Parser as Category
from bilutv.parser.channel import Parser as Channel
from bilutv.parser.movie import Parser as Movie


class Bilutv:
    domain = "http://bilutv.net"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        url = '%s%s?page=%s' % (self.domain, channel, page)
        response = Request().get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%s/xem-phim/phim-0-%s" % (self.domain, id)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, url):
        url = "%s%s" % (self.domain, url)
        response = Request().get(url)
        return Movie().get(response, True)
