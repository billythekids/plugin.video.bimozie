import urllib
from utils.mozie_request import Request
from phimgi.parser.category import Parser as Category
from phimgi.parser.channel import Parser as Channel
from phimgi.parser.movie import Parser as Movie


class Phimgi:
    domain = "https://phimgi.tv"
    replace_domain = "https://phimnhe.net"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "").replace(self.replace_domain, "")
        if page > 1:
            url = '%s%spage/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        movie_id, nonce = Movie().get_movie_link(Request().get(id))
        params = {
            'action': 'halim_ajax_show_all_eps_list',
            'episode': 1,
            'server': 1,
            'postid': movie_id
        }

        url = "%s/wp-admin/admin-ajax.php" % self.domain
        response = Request().post(url, params)
        return Movie().get(response, nonce)

    def getLink(self, movie):
        data = movie['link'].split('|') # postid|serverid|epid|nounce
        return Movie().get_link(data, self.domain)

    def search(self, text):
        text = urllib.quote_plus(text)
        url = "%s/search/%s" % (self.domain, text)
        response = Request().get(url)
        return Channel().get(response, 1)
