import re
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin


def get_link(url):
    base_url = url.rpartition('/')[0]
    res = Request()
    response = res.get(url)
    matches = re.findall('(chunklist.*)', response)

    stream_urls = []
    for m in matches:
        stream_url = base_url + '/' + m
        stream_urls.append((stream_url, m))

    arequest = AsyncRequest(res)
    results = arequest.get(list(map(lambda x: x[0], stream_urls)), parser=parse_fptplay_stream, args=base_url)
    for i in range(len(stream_urls)):
        response = response.replace(stream_urls[i][1], results[i])

    url = PasteBin().dpaste(response, name=url, expire=60)
    return url, '1080'


def parse_fptplay_stream(response, request, base_url):
    matches = re.findall('(media_.*)', response)
    for m in matches:
        stream_url = base_url + '/' + m
        response = response.replace(m, stream_url)

    url = PasteBin().dpaste(response, name=base_url, expire=60)
    return url
