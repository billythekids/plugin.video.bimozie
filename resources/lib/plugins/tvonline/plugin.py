from tvonline.parser.category import Parser as Category
from tvonline.parser.channel import Parser as Channel
from tvonline.parser.movie import Parser as Movie
from utils.mozie_request import Request


class TVOnline:
    domain = "http://www.xemtivimienphi.com"
    token = None
    member_id = None

    def __init__(self):
        self.request = Request(header={
            'User-Agent': 'Mozilla/5.0',
        }, session=True)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        url = '%s/%s' % (self.domain, channel)
        response = self.request.get(url)
        page = int(channel.replace('#', ''))
        return Channel().get(response, page)

    def getMovie(self, id):
        url = id.replace(self.domain, '')
        url = url.replace('./', '')
        url = "{}/{}".format(self.domain, url)
        response = self.request.get(url)
        return Movie().get(response, self.domain, url)

    def getLink(self, url):
        response = self.request.get(url)
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/findContent/" % self.domain
        params = {
            'term': text
        }
        response = self.request.post(url, params)
        return Channel().get(response, 1)
