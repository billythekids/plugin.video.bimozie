import urllib
from utils.mozie_request import Request
from fcine.parser.category import Parser as Category
from fcine.parser.channel import Parser as Channel
from fcine.parser.movie import Parser as Movie


class Fcine:
    domain = "https://fcine.net"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        url = '%s?alphabet=all&page=%d' % (channel, page)
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
        url = "%s/findContent/" % (self.domain)
        params = {
            'term': text
        }
        response = Request().post(url, params)
        return Channel().get(response, 1)
