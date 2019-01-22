from utils.mozie_request import Request
from phimmedia.parser.category import Parser as Category
from phimmedia.parser.channel import Parser as Channel
from phimmedia.parser.movie import Parser as Movie
import urllib


class Phimmedia:
    domain = "http://www.phimmedia.tv"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        if page > 1:
            url = '%s%s&page=%d' % (self.domain, channel, page)
        else:
            url = '%s/%s.html' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%sxem-online.html" % id
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get(response, True)

    def search(self, text, page=1):
        url = "%s/index.php?keyword=%s&do=phim&act=search&page=%s" % (self.domain, urllib.quote_plus(text), page)
        response = Request().get(url)
        return Channel().get(response)

