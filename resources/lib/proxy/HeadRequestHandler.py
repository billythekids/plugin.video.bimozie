import requests

from . import RequestHelper

streaming = False


class HeadRequestHandler:
    def __init__(self, context):
        self.context = context

    def prepare_download_header(self, is_range_suport, range_seek=0):
        request_headers = RequestHelper.extract_request_header(self.context)

        if is_range_suport:
            from_range = 0
            to_range = ''
            if 'Range' in request_headers:
                from_range, to_range = RequestHelper.extract_request_header_range(request_headers['Range'])
            request_headers.update({
                'Range': 'bytes=%s-%s' % (from_range + range_seek, to_range)
            })

        return request_headers

    def send_back_header(self, url, range_seek=0):
        is_range_support = RequestHelper.is_support_range(url)
        request_headers = self.prepare_download_header(is_range_support, range_seek=range_seek)

        response = requests.head(url, allow_redirects=True, headers=request_headers)
        RequestHelper.send_back_header(self.context, response, is_range_support, range_seek)
