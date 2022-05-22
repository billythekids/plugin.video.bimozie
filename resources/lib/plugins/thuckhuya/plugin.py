import re
from utils.mozie_request import Request
from thuckhuya.parser.channel import Parser as Channel
from thuckhuya.parser.movie import Parser as Movie


class Thuckhuya:
    # domain = "https://mitom1live.tv"
    domain = "https://json.cvndnss.com"

    def getCategory(self):
        channel = Channel.get(Request().get("{}//all_live_rooms.json".format(self.domain)))
        return [], channel

    def getMovie(self, m_id):
        response = Request().get("{}/room/{}/detail.json".format(self.domain, m_id))
        return Movie().get(response, m_id)

    def search(self, text):
        return None
