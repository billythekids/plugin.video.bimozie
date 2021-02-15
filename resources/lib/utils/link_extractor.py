# -*- coding: utf-8 -*-
import re


class LinkExtractor:
    def __init__(self):
        pass

    @staticmethod
    def iframe(txt):
        reg = re.search(r'''<iframe.*src=['|"](.*?)['|"]''', txt)
        if reg:
            print("Found iframe source: {}".format(reg.group(1)))
            return reg.group(1)

        return None
