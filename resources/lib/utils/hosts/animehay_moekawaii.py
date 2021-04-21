# -*- coding: utf-8 -*-

import re

from .. import xbmc_helper as helper
from ..mozie_request import Request


def get_link(url):
    helper.log("*********************** Apply animehay moekawaii url %s" % url)
    req = Request()

    response = req.get(url, redirect=True)
    url = re.search(r"sources:\[{file:\s'(.*?)'}", response).group(1)
    # url = "https://animehay.kyunkyun.net{}".format(url)

    return url, 'Animehay moekawaii'
