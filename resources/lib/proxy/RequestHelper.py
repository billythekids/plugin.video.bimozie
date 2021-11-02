import requests, re
from six.moves.urllib.parse import parse_qsl


def is_support_range(url):
    response = requests.head(url, allow_redirects=True, headers={
        'Range': 'bytes=0-8'
    })

    if 'Content-Length' in response.headers:
        content_size = int(response.headers['Content-Length'])
        if content_size == 9:
            return True

    return False


def extract_request_header_range(text):
    m = re.match(r'bytes=(\d+)-(\d+)?', text)
    from_range = int(m.group(1)) if m.group(1) else 0
    to_range = int(m.group(2)) if m.group(2) else ''
    return from_range, to_range


def extract_response_header_range(text):
    m = re.match(r'bytes\s-?(\d+)-(\d+)?/(\d+)?', text)
    if not m:
        return None, None, None

    from_range = int(m.group(1)) if m.group(1) else 0
    to_range = int(m.group(2)) if m.group(2) else ''
    max_range = int(m.group(3)) if m.group(3) else ''
    return from_range, to_range, max_range


def send_back_header(context, response, is_range_support=False, range_seek=0):
    # print("Response status %s" % response.status_code)
    context.send_response(response.status_code)
    # if response.status_code != 200:
    #     print(response.body)
    # context.send_response(200)
    response_headers = response.headers
    # print(response_headers)
    # self.context.send_header('Content-Type', 'application/octet-stream')

    # if 'Connection' in response_headers:
    #     data = response_headers['Connection']
    #     context.send_header('Connection', data)

    # if 'Keep-Alive' in response_headers:
    #     data = response_headers['Keep-Alive']
    #     context.send_header('Keep-Alive', data)

    if 'Accept-Ranges' in response_headers:
        data = response_headers['Accept-Ranges']
        context.send_header('Accept-Ranges', data)
    # else:
    #     context.send_header('Accept-Ranges', 'bytes')

    # if 'Content-Type' in response_headers:
    #     data = response_headers['Content-Type']
    #     context.send_header('Content-Type', data)
    # else:
    context.send_header('Content-Type', 'application/vnd.apple.mpegurl; charset=utf-8')

    if 'Content-Length' in response_headers:
        content_length = int(response_headers['Content-Length']) - range_seek
        context.send_header('Content-Length', content_length)
    else:
        content_length = len(response.content) - range_seek
        context.send_header('Content-Length', len(response.content))

    if (is_range_support or ('Content-Range' in response_headers)) and content_length > 0:
        if 'Content-Range' in response_headers and content_length:
            from_range, to_range, max_range = \
                extract_response_header_range(response_headers['Content-Range'])
            context.send_header("Content-Ranges",
                                     'bytes %s-%s/%s' % (
                                         from_range - range_seek, content_length - 1, content_length)
                                     )

    context.end_headers()


def parse_url(url):
    if '|' in url:
        parts = url.split('|')
        return parts[0], dict(parse_qsl(parts[1]))

    return url, None


def extract_request_header(context):
    headers = {}
    for key in context.headers:
        if 'Host' not in key:
            headers[key] = context.headers[key]

    return headers
