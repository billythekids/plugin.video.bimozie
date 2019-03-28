import re
import json
import HTMLParser
from utils.mozie_request import Request


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


def get_link(url):
    response = Request().get(url)
    m = re.search('data-options="(.+?)"', response)
    h = HTMLParser.HTMLParser()
    s = m.group(1)
    s = h.unescape(s)
    s = json.loads(s)
    s = json.loads(s['flashvars']['metadata'])
    items = [(i['url'], rsl(i['name'])) for i in s['videos']]
    items = sorted(items, key=lambda elem: int(elem[1]), reverse=True)
    return items[0]
