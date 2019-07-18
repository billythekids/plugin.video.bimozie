import urllib
from utils.mozie_request import Request
from xemphim.parser.category import Parser as Category
from xemphim.parser.channel import Parser as Channel
from xemphim.parser.movie import Parser as Movie
from datetime import datetime


class Xemphim:
    domain = "https://xemphim.plus"

    def getCategory(self):
        response = Request().get(self.domain)
        cat = Category().get(response)
        movies = Channel().get(response, 1)
        movies['page'] = 1
        return cat, movies

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s?page=%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = '%s%s' % (self.domain, id)
        url = Movie().get_movie_link(Request().get(url))
        url = '%s%s' % (self.domain, url)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        return Movie().get_link(movie)

    def search(self, text):
        today = datetime.now()
        d = today.strftime("%Y-%m-%d-%H")

        url = "https://b.xemphim.plus/suggestions/titles-%s.json" % d
        response = Request().get(url)
        result = Channel().search_result(response, text)
        print(result)
        return result
