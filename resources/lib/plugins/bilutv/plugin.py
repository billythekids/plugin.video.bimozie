from utils.mozie_request import Request
from bilutv.parser.category import Parser as Category
from bilutv.parser.channel import Parser as Channel
from bilutv.parser.movie import Parser as Movie
import urllib


class Bilutv:
    domain = "https://bilutv.org"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%s&page=trang-%d.html' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = Request().get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%s/phim-0-%s.html" % (self.domain, id)
        response = Request().get(url)
        url = Movie().get_movie_link(response)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = "%s/ajax/player/" % self.domain
        data = movie['link'].split(",")
        params = {
            'id': data[0],
            'ep': data[1],
            'sv': data[2]
        }
        response = Request().post(url, params)
        return Movie().get_link(response)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s.html" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response)
