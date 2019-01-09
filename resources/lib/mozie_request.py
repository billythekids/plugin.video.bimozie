import urllib
import urllib2
import cookielib


class Request:
    DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

    def __init__(self):
        self.cookies = cookielib.LWPCookieJar()
        self.handlers = (urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(self.cookies))
        self.opener = urllib2.build_opener(*self.handlers)

    def get(self, url):
        # try:
        print("Request URL: %s" % url)
        request = urllib2.Request(url, headers=self.DEFAULT_HEADERS)
        response = urllib2.urlopen(request)
        content = response.read()
        response.close()
        return content
        # except:
        #     return ""

    def post(self, url, params):
        data = urllib.urlencode(params)
        print("Post URL: %s params: %s" % (url, data))
        request = urllib2.Request(url, data=data, headers=self.DEFAULT_HEADERS)
        response = urllib2.urlopen(request)
        content = response.read()
        response.close()
        return content
