import urllib
from utils.mozie_request import Request
from vtv16.parser.category import Parser as Category
from vtv16.parser.channel import Parser as Channel
from vtv16.parser.movie import Parser as Movie


class Vtv16:
    domain = "http://94.242.62.166"

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
        url = '%s/xem-phim.html' % id
        response = Request().get(url)
        return Movie().get(response, url)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response, movie['link'])

    def search(self, text):
        url = "%s/tim-kiem-phim/%s/" % (self.domain, text.replace(' ', '-'))
        response = Request().get(url)
        return Channel().get(response, 1)
