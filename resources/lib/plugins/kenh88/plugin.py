import urllib
from utils.mozie_request import Request
from kenh88.parser.category import Parser as Category
from kenh88.parser.channel import Parser as Channel
from kenh88.parser.movie import Parser as Movie


class Kenh88:
    domain = "http://www.kenh88.com"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/page/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page, self.domain)

    def getMovie(self, id):
        url = '%s%s' % (self.domain, id.replace('/phim/', '/xem-phim-online/'))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = '%s%s' % (self.domain, movie['link'])
        response = Request().get(url)
        return Movie().get_link(response, url)

    def search(self, text):
        url = "%s/film/search?keyword=%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1, self.domain)
