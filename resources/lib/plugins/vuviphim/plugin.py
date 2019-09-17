import urllib
from utils.mozie_request import Request
from vuviphim.parser.category import Parser as Category
from vuviphim.parser.channel import Parser as Channel
from vuviphim.parser.movie import Parser as Movie


class Vuviphim:
    domain = "http://vuviphim.com"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        channel = channel.replace("https", "http")
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/page/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(Request().get(id)).replace("https", "http")
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'].replace("https", "http"))
        return Movie().get_link(response)

    def search(self, text):
        text = urllib.quote_plus(text)
        url = "%s/wp-admin/admin-ajax.php" % self.domain
        response = Request().post(url, params={
            'action': 'ajaxsearchpro_search',
            'asid': 1,
            'asp_inst_id': '1_1',
            'aspp': text,
            'options': 'current_page_id=64113&qtranslate_lang=0&asp_gen%5B%5D=title&asp_gen%5B%5D=content&customset%5B%5D=page&customset%5B%5D=post'
        })
        return Channel().search_result(response)
