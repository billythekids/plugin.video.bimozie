import re

from six.moves.urllib.parse import quote

from .mozie_request import Request

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def replace_proxy_content(content):
    urls = re.findall(r'(http.*)', content)
    for url in urls:
        proxy_url = 'http://127.0.0.1:8964?u={}'.format(quote(url))
        content = content.replace(url, proxy_url)

    return content


def replace_proxy_link(url, headers=None):
    content = Request().get(url, headers=headers)
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    urls = re.findall(r'(http.*)', content)
    for url in urls:
        if not base_url in url:
            url = "{}/{}".format(base_url, url)

        proxy_url = 'http://127.0.0.1:8964?u={}'.format(quote(url))
        content = content.replace(url, proxy_url)

    return content


def get_adaptive_link(url, headers=None):
    if headers is None:
        headers = {}
    response = Request().get(url, headers=headers)
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc

    resolutions = re.findall(r'RESOLUTION=\d+x(\d+)', response)
    matches = re.findall(r'^(?!#)(.*)', response, re.MULTILINE)
    if '2048' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '2048' == i), -1)
        url = matches[idx]
    elif '1080' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '1080' == i), -1)
        url = matches[idx]
    elif '720' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
        url = matches[idx]
    elif '480' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
        url = matches[idx]
    elif '360' in resolutions:
        idx = next((resolutions.index(i) for i in resolutions if '360' == i), -1)
        url = matches[idx]

    if not 'http' in url:
        url = "{}{}".format(base_url, url)

    return url
