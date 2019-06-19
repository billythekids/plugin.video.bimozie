import re
import json
from utils.mozie_request import Request


def get_link(url):
    req = Request()

    req.get(url, redirect=True)
    response = req.get_request()
    location = response.history[0].headers['Location']
    id = re.search('id=(.*)', location).group(1)
    # POST http://sl2.animehay.tv/vl/{id}
    response = json.loads(req.post('http://sl2.animehay.tv/vl/%s' % id, headers={
        'Referer': location
    }))
    if '720p' in response:
        create_playlist(response['720p'])

    return None


def create_playlist(data):
    print(data)
