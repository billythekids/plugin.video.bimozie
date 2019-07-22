import urllib
from utils.mozie_request import Request
from phim3s.parser.category import Parser as Category
from phim3s.parser.channel import Parser as Channel
from phim3s.parser.movie import Parser as Movie


class Phim3s:
    domain = "https://phim3s.pw/"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%spage-%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = '%s%sxem-phim/' % (self.domain, id)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = 'https://sub4.phim3s.pw/v3/?link=%s&is_encrypt=1&json=1&reload=0&s=40' % movie['link']
        response = Request().get(url)
        return Movie().get_link(response)

    def search(self, text):
        # https://phim3s.pw/ajax/film/search?keyword=bao+thanh+thien
        url = "%sajax/film/search?keyword=%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().search(response, 1)
