import urllib, re
from utils.mozie_request import Request
from anime47.parser.category import Parser as Category
from anime47.parser.channel import Parser as Channel
from anime47.parser.movie import Parser as Movie

user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept-Encoding': 'utf-8'
}


class anime47:
    domain = "https://anime47.com"

    def __init__(self):
        self.request = Request(h, session=True)

    def getCategory(self):
        response = self.request.get('{}/'.format(self.domain), headers=h)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        print(channel)
        if page > 1:
            if channel.endswith(".html"):
                url = re.sub(r'\d+.html', '{}.html'.format(page), ('%s%s' % (self.domain, channel)))
            else:
                url = '%s/%s&page=%d' % (self.domain, channel, page)

            print(url)
        else:
            url = '%s/%s' % (self.domain, channel)
        response = self.request.get(url, headers=h)
        return Channel().get(response, page)

    def getMovie(self, movie_id):
        url = "%s%s" % (self.domain, movie_id)
        url = Movie().get_movie_link(self.request.get(url, headers=h))
        url = "%s/%s" % (self.domain, url)
        response = self.request.get(url, headers=h)
        return Movie().get(response, url)

    def getLink(self, movie):
        url = movie['link'].replace(self.domain, '')
        url = "%s/%s" % (self.domain, url)
        response = self.request.get(url, headers=h)
        return Movie().get_link(response, self.domain, url, self.request)

    def search(self, text):
        url = "%s/tim-nang-cao/?keyword=%s" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url, headers=h)
        return Channel().get(response, 1)
