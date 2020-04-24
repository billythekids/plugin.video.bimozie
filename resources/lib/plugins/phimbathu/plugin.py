import urllib
from utils.mozie_request import Request, user_agent
from phimbathu.parser.category import Parser as Category
from phimbathu.parser.channel import Parser as Channel
from phimbathu.parser.movie import Parser as Movie
from cloudscraper2 import CloudScraper
import urllib, pickle, time
import utils.xbmc_helper as helper


class Phimbathu:
    domain = "https://phimbathu.org"

    def __init__(self):
        if helper.has_file_path('phimbathu.bin') and helper.get_last_modified_time_file('phimbathu.bin') + 43200 > \
                int(time.time()):
            with open(helper.get_file_path('phimbathu.bin')) as f:
                self.cookies = pickle.load(f)
        else:
            self.updateSession(self.domain)
        self.request = Request()

    def updateSession(self, url, delay=10):
        scraper = CloudScraper.create_scraper(delay=delay)
        scraper.headers.update({'User-Agent': user_agent})
        self.cookies = scraper.get(url).cookies.get_dict()
        if not helper.has_file_path('phimbathu.bin'):
            helper.write_file('phimbathu.bin', '')

        with open(helper.get_file_path('phimbathu.bin'), 'wb+') as f:
            pickle.dump(self.cookies, f)

    def getCategory(self):
        response = self.request.get(self.domain, cookies=self.cookies)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%s&page=trang-%d.html' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url, cookies=self.cookies)
        return Channel().get(response)

    def getMovie(self, id):
        url = "%s/phim-0-%s.html" % (self.domain, id)
        response = self.request.get(url, cookies=self.cookies)
        url = Movie().get_movie_link(response)
        response = self.request.get(url, cookies=self.cookies)
        return Movie(self.cookies).get(response, self.request)

    def getLink(self, movie):
        response = self.request.get(movie['link'], cookies=self.cookies)
        return Movie(self.cookies).get_link(response, self.domain, movie['link'], self.request)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s.html" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url, cookies=self.cookies)
        return Channel().get(response)
