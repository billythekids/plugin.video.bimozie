# -*- coding: utf-8 -*-

import re

import utils.xbmc_helper as helper
from utils.mozie_request import Request


def get_link(url):
    helper.log("*********************** Apply animehay cca url %s" % url)
    req = Request()

    response = req.get(url, redirect=True)
    url = re.search(' data-file="(.*?)"', response).group(1)

    return url, 'Animehay CCA'
