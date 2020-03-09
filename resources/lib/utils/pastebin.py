# -*- coding: utf-8 -*-
import json
import requests
import utils.xbmc_helper as helper


class PasteBin:
    def __init__(self, api_dev_key=None):
        self.api_dev_key = api_dev_key

    def pastehaste(self, content, name="", expire=1440):
        url = 'https://hastebin.com/documents'
        response = requests.post(url, content.encode('utf-8'), timeout=10)
        dockey = json.loads(response.text)['key']
        return "https://hastebin.com/raw/" + dockey

    def dpaste_deprecated(self, content, name="", expire=1440):
        url = 'https://dpaste.de/api/'
        params = {
            'lexer ': 'text',
            'content': content,
            'expire': 3600,
            'format': 'url'
        }
        r = requests.post(url, data=params, timeout=30)

        if r.status_code == requests.codes.ok:
            url = r.text.replace('\n', '') + '/raw'
            print('Dpaste url: %s' % url)
            return url

    def dpaste_deprecated_2(self, content, name="", expire=1440):
        print("Uploading playlist")
        url = 'https://hastebin.com/documents'
        params = content
        r = requests.post(url,
                          data=params,
                          timeout=30)

        resp = json.loads(r.text)
        url = "https://hastebin.com/raw/%s" % resp['key']
        print('hastebin url: %s' % url)
        return url

    def dpaste(self, content, name="", expire=1440):
        print("Uploading playlist")
        url = 'https://paste.kodi.tv/documents'
        params = content
        r = requests.post(url,
                          data=params,
                          timeout=30)

        resp = json.loads(r.text)
        url = "https://paste.kodi.tv/raw/%s" % resp['key']
        print('hastebin url: %s' % url)
        return url
