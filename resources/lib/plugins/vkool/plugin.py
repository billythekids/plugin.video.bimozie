from utils.mozie_request import Request
from vkool.parser.category import Parser as Category
from vkool.parser.channel import Parser as Channel
from vkool.parser.movie import Parser as Movie
import urllib


class Vkool:
    domain = "http://phim.vkool.tv"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%s%d.html' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = Request().get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%s/xemphim/-%s-xem-phim.html" % (self.domain, id)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response, self.domain)

    def search(self, text, page=1):
        url = "%s/search/%s.html" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response)
