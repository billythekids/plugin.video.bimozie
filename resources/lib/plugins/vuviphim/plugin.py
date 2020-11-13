import urllib
from utils.mozie_request import Request
from vuviphim.parser.category import Parser as Category
from vuviphim.parser.channel import Parser as Channel
from vuviphim.parser.movie import Parser as Movie


class Vuviphim:
    domain = "https://vuviphimz.net"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        # channel = channel.replace("https", "http")
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/page/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        # url = Movie().get_movie_link(Request().get(id)).replace("https", "http")
        url = Movie().get_movie_link(Request().get(id))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        # response = Request().get(movie['link'].replace("https", "http"))
        response = Request().get(movie['link'])
        return Movie().get_link(response, movie['link'])

    def search(self, text):
        # text = urllib.quote_plus(text)
        url = "%s/wp-json/dooplay/search/" % self.domain
        response = Request().get(url, params={
            'keyword': text,
            'nonce': '1b88282004'
        })
        return Channel().search_result(response)
