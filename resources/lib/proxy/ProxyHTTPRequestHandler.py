import time
import BaseHTTPServer
import httplib as HTTPStatus
try:
    from urlparse import urlparse, parse_qsl
except ImportError:
    from urllib.parse import urlparse, parse_qsl

from .GetRequestHandler import GetRequestHandler
from .HeadRequestHandler import HeadRequestHandler

streaming = False


class ProxyHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    handler = None
    # wbufsize = 1024 * 1024

    def _parse_url(self):
        p = urlparse(self.path)
        q = dict(parse_qsl(p.query))

        if 'u' not in q:
            self.send_error(404)
            return

        return q['u']

    def _get_url(self):
        u = self._parse_url()
        return u[:-3] if u.endswith('-no') or u.endswith('-dl') else u

    def _is_truncate(self):
        u = self._parse_url()
        return False if u.endswith('-no') or u.endswith('-dl') else True

    def _is_downloadable(self):
        u = self._parse_url()
        return u.endswith('-dl')

    def _is_streaming(self):
        u = self._parse_url()
        return u.endswith('-no')

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(
                    HTTPStatus.NOT_IMPLEMENTED,
                    "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            # self.wfile.flush() #actually send the response if not already done.
        except Exception as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
            return

    def do_HEAD(self):
        url = self._get_url()
        handler = HeadRequestHandler(self)
        need_truncate = self._is_truncate()
        if need_truncate:
            handler.send_back_header(url, 8)
        else:
            handler.send_back_header(url)

        print("finish do_HEAD")
        return

    def do_GET(self):
        url = self._get_url()
        if not self.handler:
            self.handler = GetRequestHandler(self)

        print('proxy request get: %s' % url)

        if self._is_truncate():
            print("Downloading with truncate do_GET")
            self.handler.download_content(url)
            # self.handler.stream_content(url, 8)
        elif self._is_downloadable():
            print("Downloading do_GET")
            self.handler.download_content(url, 0)
        elif self._is_streaming():
            print("Streaming do_GET")
            self.handler.stream_content(url)

        print("finish do_GET")
        return
