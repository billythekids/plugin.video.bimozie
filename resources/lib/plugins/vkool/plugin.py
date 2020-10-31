from utils.mozie_request import Request
from vkool.parser.category import Parser as Category
from vkool.parser.channel import Parser as Channel
from vkool.parser.movie import Parser as Movie
import urllib

user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


class Vkool:
    domain = "http://movie.vkool.net"
    # replace_domain = "http://phim.vkool.net"

    def __init__(self):
        self.request = Request(h, session=True)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%s%d.html' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%s/xemphim/-%s-xem-phim.html" % (self.domain, id)
        response = self.request.get(url)
        return Movie().get(response)

    def getLink(self, movie):
        r = self.request
        response = r.get(movie['link'])
        return Movie().get_link(response, self.domain, movie['link'], r)

    def search(self, text, page=1):
        url = "%s/search/%s.html" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response)
