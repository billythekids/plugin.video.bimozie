import urllib
from utils.mozie_request import Request
from phimbathu.parser.category import Parser as Category
from phimbathu.parser.channel import Parser as Channel
from bilutv.parser.movie import Parser as Movie


class Phimbathu:
    domain = "http://phimbathu.org/"

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
        return Channel().get(response, page)

    def getMovie(self, id):
        url = "%sphim-0-%s.html" % (self.domain, id)
        response = Request().get(url)
        url = Movie().get_movie_link(response)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = "%sajax/player" % self.domain
        data = movie['link'].split(",")
        params = {
            'id': data[0],
            'ep': data[1],
            'sv': data[2]
        }
        response = Request().post(url, params)
        return Movie().get_link(response)

    def search(self, text):
        # http://phimbathu.org/tim-kiem/(keywords).html
        url = "%stim-kiem/%s.html" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
