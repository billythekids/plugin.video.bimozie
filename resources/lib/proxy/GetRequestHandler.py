import time

import requests
from requests import HTTPError

from . import RequestHelper

streaming = False


class GetRequestHandler:
    def __init__(self, context):
        self.context = context

    def stream_content(self, url, need_truncate=False, headers=None):
        pass

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

        return request_headers

    def download_content(self, url, range_seek=8):
        # is_range_support = RequestHelper.is_support_range(url)
        is_range_support = False
        request_headers = self.prepare_download_header(is_range_support, range_seek=range_seek)
        # print('request_headers', request_headers)

        response = requests.get(url, allow_redirects=True, headers=request_headers)
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

        def stream2():
            r = requests.get(url, stream=True)
            self.context.wfile.write(r.raw.read())

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
                print(e)
                if retry > 0:
                    print('retry %s' % retry)
                    time.sleep(3000)
                    retry = retry - 1
                    print('retry %s' % retry)
                    # r.close()
                    # stream(retry)

            r.close()

        stream()
