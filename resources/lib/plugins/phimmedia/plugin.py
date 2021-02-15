from utils.mozie_request import Request
from phimmedia.parser.category import Parser as Category
from phimmedia.parser.channel import Parser as Channel
from phimmedia.parser.movie import Parser as Movie
from cloudscraper2 import CloudScraper
import pickle, time
import utils.xbmc_helper as helper
import urllib


user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Host': 'www.phimmedia.tv',
    # 'Referer': 'www.phimmedia.tv'
}


class Phimmedia:
    replace_domain = "https://www.phimmedia.me"
    domain = "https://www.phimmedia.me"
    cookies = {}

    def __init__(self):
        self.request = Request(h, session=True)

    def updateSession(self, url, delay=10):
        try:
            scraper = CloudScraper.create_scraper(delay=delay)
            scraper.headers.update({'User-Agent': user_agent})
            self.cookies = scraper.get(url).cookies.get_dict()
            with open(helper.get_file_path('phimmedia.bin'), 'wb') as f:
                pickle.dump(self.cookies, f)
        except: pass

    def getCategory(self):
        response = self.request.get("{}/".format(self.domain))
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.replace_domain, "").replace(self.domain, "")

        if page > 1:
            url = '%s%s&page=%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%sxem-online.html" % id
        response = self.request.get(url)
        return Movie().get(response)

    def getLink(self, movie):
        movie_link = movie['link'].replace(self.replace_domain, self.domain)

        response = self.request.get(movie_link)
        return Movie().get_link(response, movie['link'])

    def search(self, text, page=1):
        url = "%s/index.php?keyword=%s&do=phim&act=search&page=%s" % (self.domain, urllib.quote_plus(text), page)
        response = self.request.get(url)
        return Channel().get(response)
