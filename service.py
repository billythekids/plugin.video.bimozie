#! /usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/D4anielCB/plugin.video.Cinput/issues/1

import threading
import xbmc
import sys
import os
import socket
from SocketServer import ThreadingMixIn

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, 'resources', 'lib'))
sys.path.append(os.path.join(current_dir, 'resources', 'lib', 'proxy'))

from resources.lib.utils import xbmc_helper as helper
from resources.lib.proxy.ProxyHTTPRequestHandler import ProxyHTTPRequestHandler
from BaseHTTPServer import HTTPServer


class Server(HTTPServer):
    """HTTPServer class with timeout."""

    def get_request(self):
        """Get the request and client address from the socket."""
        self.socket.settimeout(5.0)
        result = None
        while result is None:
            try:
                result = self.socket.accept()
            except socket.timeout:
                pass
        result[0].settimeout(1000)
        return result


class ThreadingHTTPServer(ThreadingMixIn, Server):
    """Handle requests in a separate thread."""


def run():
    server_class = ThreadingHTTPServer
    httpd = server_class(('127.0.0.1', 8964), ProxyHTTPRequestHandler)
    helper.message('Local proxy started', 'Proxy')

    while not xbmc.abortRequested:
        httpd.handle_request()
    httpd.server_close()


if __name__ == "__main__":
    run()
