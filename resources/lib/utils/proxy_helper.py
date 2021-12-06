import re

from six.moves.urllib.parse import quote

from .mozie_request import Request

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def prepend_url(url, ext=None):
    return 'http://127.0.0.1:8964?u={}{}'.format(quote(url), ext or '')


def _prepare_content(content, base_url=None, replace_fn=None):
    extinf_blocks = re.findall(r'(?s)(#extinf.*?)(?=\n#extinf)', content, re.IGNORECASE)
    for extinf_block in extinf_blocks:
        if 'EXT-X-BYTERANGE' in extinf_block.upper():
            continue

        origin_url = extinf_block.split('\n')[-1]
        if not 'http' in origin_url:
            full_url = "{}/{}".format(base_url, origin_url)
            content = content.replace(origin_url, full_url)
            origin_url = full_url

        if callable(replace_fn):
            content = content.replace(origin_url, prepend_url(replace_fn(origin_url)))
        else:
            content = content.replace(origin_url, prepend_url(origin_url))

    return content


def replace_proxy_content(content, base_url=None):
    return _prepare_content(content, base_url)


def replace_proxy_link(url, headers=None, replace_fn=None):
    content = Request().get(url, headers=headers)
    base_url = urlparse(url)
    base_url = '{}://{}/{}'.format(base_url.scheme, base_url.netloc, '/'.join(base_url.path.split('/')[1:-1]))

    return _prepare_content(content, base_url=base_url, replace_fn=replace_fn)


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
