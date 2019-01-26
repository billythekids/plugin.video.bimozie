# -*- coding: utf-8 -*-
from utils.mozie_request import Request
import utils.xbmc_helper as helper
from utils.fshare import FShare
import re
import HTMLParser
import json


def rsl(s):
    s = str(s).replace('HDG', '') \
        .replace('HD', '1080') \
        .replace('SD', '640') \
        .replace('large', '640') \
        .replace('lowest', '240') \
        .replace('low', '480') \
        .replace('hd', '720') \
        .replace('fullhd', '1080') \
        .replace('Auto', '640') \
        .replace('medium', '240') \
        .replace('mobile', '240') \
        .replace('AUTO', '640')

    result = re.search('(\d+)', s)
    if result:
        return result.group(1)
    else:
        return '240'


class LinkParser:
    def __init__(self, url):
        self.url = url

    def get_link(self):
        print("Find link source of %s" % self.url)
        if re.search('ok.ru', self.url):
            self.url.replace('?autoplay=1', '')
            return self.get_link_ok()
        if re.search('openload.co', self.url):
            return self.get_link_openload()
        if re.search('fshare.vn', self.url):
            return self.get_link_fshare()
        if re.search('dailymotion.com', self.url):
            return self.get_link_dailymotion()

        return self.url

    def get_link_ok(self):
        response = Request().get(self.url)
        m = re.search('data-options="(.+?)"', response)
        h = HTMLParser.HTMLParser()
        s = m.group(1)
        s = h.unescape(s)
        s = json.loads(s)
        s = json.loads(s['flashvars']['metadata'])
        items = [(i['url'], rsl(i['name'])) for i in s['videos']]
        items = sorted(items, key=lambda elem: int(elem[1]), reverse=True)
        return items[0]

    def get_link_openload(self):
        try:
            import resolveurl
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_dailymotion(self):
        try:
            import resolveurl
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_fshare(self):
        if helper.getSetting('fshare.enable'):
            return FShare(
                self.url,
                helper.getSetting('fshare.username'),
                helper.getSetting('fshare.password')
            ).get_link(), '1080'
        else:
            return FShare(self.url).get_link(), '1080'
