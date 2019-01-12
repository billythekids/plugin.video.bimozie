# coding: utf8
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
        response = Request().get(self.url)
        m = re.search('data-options=\"([^\"]+)\"', response)
        h = HTMLParser.HTMLParser()
        m = h.unescape(m.group(1))
        m = re.search('\"metadata\":\"(.*})\",', m).group(1).replace('\\', '')
        m = re.search('"videos":(.*]),"meta', m).group(1)
        m = json.loads(m)
        link = m[-1]
        link = link[u'url'].replace('u0026', '&')
        link = link.encode('utf-8').replace('UNKNOWN', 'ÇHROME')
        return link
