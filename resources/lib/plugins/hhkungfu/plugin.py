import re

from hhkungfunew.parser.category import Parser as Category
from hhkungfunew.parser.channel import Parser as Channel
from hhkungfunew.parser.movie import Parser as Movie
from utils.mozie_request import Request


class Hhhkungfu:
    domain = "https://hhhkungfu.tv"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        if page > 1:
            url = f'{channel}/page/{page}'
        else:
            url = channel
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = '%s' % (id)
        url = Movie().get_movie_link(Request().get(url))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = '%s' % (movie['link'])
        response = Request().get(url)
        return Movie().get_link(response, self.domain, url)

    def search(self, text):
        url = "%s/search/%s" % (self.domain, text)
        response = Request().get(url)
        return Channel().search_result(response)
