import urllib
import re
import base64
from utils.mozie_request import Request
from tvhay.parser.category import Parser as Category
from tvhay.parser.channel import Parser as Channel
from tvhay.parser.movie import Parser as Movie


class Tvhay:
    domain = "http://tvhay.org/"

    def __init__(self):
        self.request = Request(session=True)
        body = self.request.get(self.domain)
        # get js cookie
        r = re.search("S='(.*)';L", body)
        code = base64.b64decode(r.group(1)).replace('\n', '').replace(" ", "").replace('+"="+s+\'', '')
        code = re.findall(r'\w=([^;]+)', code)
        print(code[0])
        a = re.sub(r'(.*)\.substr\((\d),(\d)\)', r'\1[\2:\3]', code[0])
        a = re.sub(r'(.*)\.slice\((\d),(\d)\)', r'\1[\2:\3]', a)
        a = re.sub(r'(.*)\.charAt\((\d)\)', r'\1[\2]', a)
        print(a)


    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%spage/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(Request().get(id))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%ssearch/%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
