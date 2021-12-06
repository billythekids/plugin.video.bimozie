#! /usr/bin/env python

# -*- coding: utf-8 -*-
import threading
import xbmc
from resources.lib.utils import xbmc_helper as helper
from resources.lib.proxy.ProxyHTTPRequestHandler import ProxyHTTPRequestHandler
from http.server import HTTPServer, ThreadingHTTPServer
from socketserver import ThreadingMixIn

# https://github.com/D4anielCB/plugin.video.Cinput/issues/1


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run():
    server_address = ('', 8964)
    httpd = ThreadingHTTPServer(server_address, ProxyHTTPRequestHandler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()
    print("Starting server")
    # httpd.serve_forever()

    monitor = xbmc.Monitor()
    helper.message('Local proxy started', 'Proxy')

    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            break

    httpd.shutdown()
    httpd.socket.close()
    server_thread.join()
    server_thread = None
    httpd = None


if __name__ == "__main__":
    run()
