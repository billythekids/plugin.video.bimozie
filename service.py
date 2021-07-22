# -*- coding: utf-8 -*-
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

import requests
import xbmc

from resources.lib.utils import xbmc_helper as helper


# https://github.com/D4anielCB/plugin.video.Cinput/issues/1
class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'

    def getSize(self, url):
        response = requests.head(url, allow_redirects=True)
        content_size = int(response.headers['Content-Length'])
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print(url)
        print(response.headers)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        return content_size

    def do_GET(self):
        p = urlparse(self.path)
        q = dict(parse_qsl(p.query))

        if 'u' not in q:
            self.send_error(404)
            return

        u = q['u']
        url = u[:-3] if u.endswith('-no') else u
        headers = {'Range': 'bytes=8-'}
        res = requests.get(url, headers=headers)
        ret = res.content

        # for key in res.headers:
        #     self.send_header(key, res.headers[key])

        self.send_header('Content-Disposition', 'inline; filename="unnamed.png"')
        self.send_header('Content-Length', res.headers['Content-Length'])
        self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
        self.end_headers()
        self.wfile.write(ret)


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8964)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    # httpd.serve_forever()

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()

    monitor = xbmc.Monitor()

    helper.message('Local proxy started', 'Proxy')

    while not monitor.waitForAbort(3):
        pass

    httpd.shutdown()
    server_thread.join()
