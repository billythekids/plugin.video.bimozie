import re, json
from utils.mozie_request import Request
import utils.xbmc_helper as helper


def get_link(url):
    response = Request().get(url)
    sources = re.search(r'sources:\s?(.*?),\n', response)
    sources = helper.convert_js_2_json(sources.group(1).encode('utf-8'))
    if sources:
        try:
            sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
        except:
            pass

        if len(sources) > 0:
            for source in sources:
                return source.get('file')
