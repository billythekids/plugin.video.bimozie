# -*- coding: utf-8 -*-
import json
import re
from . import xbmc_helper as helper


class LinkExtractor:
    def __init__(self):
        pass

    @staticmethod
    def iframe(txt):
        reg = re.search(r'''<iframe.*src=['|"](.*?)['|"]''', txt)
        if reg:
            helper.log("Found iframe source: {}".format(reg.group(1)))
            return reg.group(1)

        return None

    @staticmethod
    def play_sources(txt):
        reg = re.search(r'sources:\s?(\[.*?\])', txt, re.DOTALL)
        if reg:
            helper.log("Found iframe source: {}".format(reg.group(1)))
            return helper.convert_js_2_json(reg.group(1))
        return None
