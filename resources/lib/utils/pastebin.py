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

    def dpaste(self, content, name="", expire=1440):
        print("Uploading playlist")
        url = 'https://api.paste.ee/v1/pastes'
        params = {
            'encrypted': 'false',
            'description': name,
            'sections': [{
                'syntax': 'text',
                'contents': content,
            }]
        }
        r = requests.post(url,
                          json=params,
                          timeout=30,
                          headers={'X-Auth-Token': 'uhE2lTkFfBMe6jdHPrXUaeSTK4p7X01KScOwFeCWQ'})

        resp = json.loads(r.text)
        url = "https://paste.ee/r/%s" % resp['id']
        print('Dpaste url: %s' % url)
        retry = 0
        while retry < 5:
            try:
                print('Retry %d' % retry)
                response = requests.get(url)
                print(response.status_code)
                if response.status_code == requests.codes.ok: break
                url += "/%d" % retry
            except:
                pass
            finally:
                retry += 1

        return url
