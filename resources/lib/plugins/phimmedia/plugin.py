from utils.mozie_request import Request
from phimmedia.parser.category import Parser as Category
from phimmedia.parser.channel import Parser as Channel
from phimmedia.parser.movie import Parser as Movie
import urllib

user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host': 'www.phimmedia.tv',
    'Referer': 'www.phimmedia.tv'
}


class Phimmedia:
    domain = "https://www.phimmedia.tv"

    def __init__(self):
        self.request = Request(h, session=True)
        self.request.post('https://www.phimmedia.tv/mak.php', params={
            'mak_firewall_redirect': self.domain,
            'mak_firewall_postcontent': ''
        })

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        if page > 1:
            url = '%s%s&page=%d' % (self.domain, channel, page)
        else:
            url = '%s/%s.html' % (self.domain, channel)
        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%sxem-online.html" % id
        response = self.request.get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = self.request.get(movie['link'])
        return Movie().get_link(response, movie['link'])

    def search(self, text, page=1):
        url = "%s/index.php?keyword=%s&do=phim&act=search&page=%s" % (self.domain, urllib.quote_plus(text), page)
        response = self.request.get(url)
        return Channel().get(response)
