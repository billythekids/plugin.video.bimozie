import json
import requests


class PasteBin:
    def __init__(self, api_dev_key=None):
        self.api_dev_key = api_dev_key

    def paste(self, content, name="", expire=1440):
        url = 'https://hastebin.com/documents'
        response = requests.post(url, content.encode('utf-8'), timeout=10)
        dockey = json.loads(response.text)['key']
        return "https://hastebin.com/raw/" + dockey
