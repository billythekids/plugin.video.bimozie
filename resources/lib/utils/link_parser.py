from mozie_request import Request
import re
import urllib
import HTMLParser
import json


class LinkParser:
    def __init__(self, url):
        self.url = url

    def get_link(self):
        if re.search('ok.ru', self.url):
            return self.get_link_ok()

        return self.url

    def get_link_ok(self):
        # response = Request().get(self.url)
        #
        # m = re.search('data-options=\"([^\"]+)\"', response)
        # h = HTMLParser.HTMLParser()
        # content = h.unescape(m.group(1))
        # m = re.search('\"metadata\":\"(.*})\",', content).group(1)
        # m = re.search('\"videos\":(\[.*}\]),', m).group(1)
        # print(m)

        # m = re.search(";(?P<hlsurl>[^;]+video\.m3u8.+?)\\&quot;", response)
        # print(m.group(1).replace(u'\\\\u0026', u'&'))

        return self.url