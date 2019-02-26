import json
import requests


class PasteBin:
    def __init__(self, api_dev_key=None):
        self.api_dev_key = api_dev_key

    def pastehaste(self, content, name="", expire=1440):
        url = 'https://hastebin.com/documents'
        response = requests.post(url, content.encode('utf-8'), timeout=10)
        dockey = json.loads(response.text)['key']
        return "https://hastebin.com/raw/" + dockey

    def dpaste(self, content, name="", expire=1440):
        url = 'https://dpaste.de/api/'
        params = {
            'lexer ': 'text',
            'content': content,
            'expire': 3600,
            'format': 'url'
        }
        r = requests.post(url, data=params, timeout=30)

        if r.status_code == requests.codes.ok:
            return r.text.replace('\n', '') + '/raw'