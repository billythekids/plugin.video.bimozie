from bilutv.parser.category import Parser as Category
from bilutv.parser.channel import Parser as Channel
from bilutv.parser.movie import Parser as Movie
from six.moves.urllib.parse import quote_plus
from utils.mozie_request import Request


class Bilutv:
    domain = "https://biluhay.net"

    def getCategory(self):
        url = "%s/%s" % (self.domain, 'danh-sach/')
        response = Request().get(url)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%s/trang-%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = Request().get(url)
        return Channel().get(response)

    def getMovie(self, mid):
        # url = "%s/phim/%s-0000.html" % (self.domain, id)
        response = Request().get(mid)
        url = Movie().get_movie_link(response)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response, self.domain)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s.html" % (self.domain, quote_plus(text))
        response = Request().get(url)
        return Channel().get(response)
