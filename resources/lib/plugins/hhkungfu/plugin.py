from hhkungfu.parser.category import Parser as Category
from hhkungfu.parser.channel import Parser as Channel
from hhkungfu.parser.movie import Parser as Movie
from six.moves.urllib.parse import quote_plus
from utils.mozie_request import Request
from . import per_page

user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept-Encoding': 'utf-8'
}


class hhkungfu:
    domain = "https://www.hhkungfu.tv"
    feed = "https://www.blogger.com/feeds/1559526659989711085/posts/default"

    def __init__(self):
        self.request = Request(h, session=True)

    def getCategory(self):
        response = self.request.get('{}{}'.format(self.feed, '?max-results={}&start-index=1'.format(per_page)), headers=h)
        return [], Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        channel = '{}{}'.format(self.feed, channel)
        response = self.request.get(channel, headers=h)
        return Channel().get(response, page)

    def getMovie(self, movie_url):
        response = self.request.get(movie_url, headers=h)
        movie_url = Movie.get_play_link(response)
        response = self.request.get(movie_url, headers=h)
        return Movie.get(response, movie_url)

    def getLink(self, movie):
        return Movie().get_link(movie['link'], self.domain, movie['originUrl'], self.request)

    def search(self, text):
        url = "%s/tim-nang-cao/?keyword=%s" % (self.domain, quote_plus(text))
        response = self.request.get(url, headers=h)
        return Channel().get(response, 1)
