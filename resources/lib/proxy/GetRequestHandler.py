import time

import requests

try:
    from cloudscraper2 import CloudScraper
except:
    import cloudscraper as CloudScraper
from requests import HTTPError

from . import RequestHelper

streaming = False

import logging
# The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class GetRequestHandler:
    def __init__(self, context):
        self.context = context
        session = requests.Session()
        self.scraper = CloudScraper.create_scraper(debug=False, sess=session)
        # self.scraper = requests.session()

    def prepare_download_header(self, is_range_support, range_seek=0):
        request_headers = RequestHelper.extract_request_header(self.context)

        if is_range_support:
            from_range = 0
            to_range = ''
            if 'Range' in request_headers:
                from_range, to_range = RequestHelper.extract_request_header_range(request_headers['Range'])
            request_headers.update({
                'Range': 'bytes=%s-%s' % (from_range + range_seek, to_range)
            })

        request_headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'
        })

        return request_headers

    def download_content(self, url, range_seek=8):
        # is_range_support = RequestHelper.is_support_range(url)
        is_range_support = False
        # request_headers = self.prepare_download_header(is_range_support, range_seek=range_seek)
        # print('request_headers', request_headers)
        url, request_headers = RequestHelper.parse_url(url)

        print('request url', url)
        if not request_headers:
            request_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.38'
            }
        else:
            print('custom request header', request_headers)

        self.scraper.headers.update(request_headers)
        response = self.scraper.get(url, proxies={'http':'209.141.55.228:80'})
        # response = requests.get(url, headers=request_headers)
        content = response.content
        if not is_range_support and range_seek > 0:
            content = content[range_seek:]

        RequestHelper.send_back_header(self.context, response, is_range_support, range_seek)
        self.context.wfile.write(content)
        self.context.wfile.flush()
        # print("send back content")

    def stream_content(self, url, range_seek=0):
        is_range_support = RequestHelper.is_support_range(url)
        request_headers = self.prepare_download_header(is_range_support, range_seek=0)
        chunk_size = 1024 * 1024 * 1

        response = requests.head(url, allow_redirects=True, headers=request_headers)
        RequestHelper.send_back_header(self.context, response)

        def stream(retry=3):
            seek = False
            try:
                with requests.get(url, stream=True, allow_redirects=True, headers=request_headers) as r:
                    r.raise_for_status()
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if not chunk:
                            print('no chunk')
                            break
                        if self.context.wfile.writable() and not self.context.close_connection:
                            if not seek and range_seek > 0:
                                chunk = chunk[range_seek:]
                                seek = True
                            self.context.wfile.write(chunk)
                            print("send trunk content %s" % len(chunk))
                        else:
                            print('Not writeable')
                            break
                    self.context.wfile.flush()
                    print("Streaming completed.")
            except HTTPError as e:
                if retry > 0:
                    print('retry %s' % retry)
                    time.sleep(3000)
                    retry = retry - 1
                    print('retry %s' % retry)
                    # r.close()
                    # stream(retry)

            r.close()

        stream()
