import urllib
from utils.mozie_request import Request
from phimmoi.parser.category import Parser as Category
from phimmoi.parser.channel import Parser as Channel
from phimmoi.parser.movie import Parser as Movie

user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Host': 'http://www.phimmoizz.net',
    # 'Referer': 'http://www.phimmoizz.net/vn.php'
}

class Phimmoi:
    domain = "http://www.phimmoizz.net"

    def __init__(self):
        self.request = Request(h, session=True)
        self.request.get('{}/vn.php'.format(self.domain))

    def getCategory(self):
        response = self.request.get('{}/'.format(self.domain), headers=h)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s/%spage-%d.html' % (self.domain, channel, page)
        else:
            url = '%s/%s' % (self.domain, channel)
        response = self.request.get(url, headers=h)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = "%s/%sxem-phim.html" % (self.domain, id)
        response = self.request.get(url, headers=h)
        return Movie().get(response, url)

    def getLink(self, movie):
        url = movie['link'].replace(self.domain, '')
        url = "%s/%s" % (self.domain, url)
        response = self.request.get(url, headers=h)
        return Movie().get_link(response, url, self.request)

    def search(self, text):
        url = "%s/tim-kiem/%s/" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url, headers=h)
        return Channel().get(response, 1)
