import urllib
from utils.mozie_request import Request
from phim14.parser.category import Parser as Category
from phim14.parser.channel import Parser as Channel
from phim14.parser.movie import Parser as Movie


class Phim14:
    domain = "http://phim14.net"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), Channel().get(response, 1, self.domain)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html', '')
            url = '%s%s/page-%d.html' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page, self.domain)

    def getMovie(self, id):
        url = '%s' % id.replace('/phim/', '/xem-phim/')
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = '%s/ajax/episode.html?do=load_episode&episodeid=%s' % (self.domain, movie['link'])
        response = Request().get(url)
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/search/%s.html" % (self.domain, text.replace(' ', '-'))
        response = Request().get(url)
        return Channel().get(response, 1, self.domain)
