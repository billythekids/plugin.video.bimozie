import re
from urlparse import urlparse
from utils.mozie_request import Request, AsyncRequest
from utils.pastebin import PasteBin


def get_link(url):
    play_list = ""
    base_url = urlparse(url)
    base_url = base_url.scheme + '://' + base_url.netloc
    resp = Request().get(url)
    resolutions = re.findall('RESOLUTION=\d+x(\d+)', resp)
    matches = re.findall('(/drive/.*)', resp)

    if len(resolutions) > 1:
        play_list += "#EXTM3U\n"
        if '1080' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            play_list += "#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1920x1080\n"
            play_list += "%s\n" % create_imacdn_stream(stream_url, base_url)
        elif '720' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '720' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            play_list += "#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=1280x720\n"
            play_list += "%s\n" % create_imacdn_stream(stream_url, base_url)
        elif '480' in resolutions:
            idx = next((resolutions.index(i) for i in resolutions if '480' == i), -1)
            url = matches[idx]
            stream_url = base_url + url
            play_list += "#EXT-X-STREAM-INF:BANDWIDTH=750000,RESOLUTION=854x480\n"
            play_list += "%s\n" % create_imacdn_stream(stream_url, base_url)
    else:
        play_list = resp
        for m in matches:
            stream_url = base_url + m
            play_list = play_list.replace(m, create_imacdn_stream(stream_url, base_url))

    url = PasteBin().dpaste(play_list, name=url, expire=60)
    return url, 'hls5'

def create_imacdn_stream(url, base_url):
    retry = 5
    res = Request()
    response = None
    while retry >= 0:
        try:
            print('Retry %d' % retry)
            response = res.get(url)
            if response != 'error': break
        except:
            pass
        finally:
            retry -= 1

    if response:
        matches = re.findall('(/drive/hls/.*)', response)
        for m in matches:
            stream_url = base_url + m
            response = response.replace(m, stream_url)

    url = PasteBin().dpaste(response, name=url, expire=60)
    return url