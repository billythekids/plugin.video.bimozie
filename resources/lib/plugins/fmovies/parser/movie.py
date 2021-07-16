# -*- coding: latin1 -*-
import re

import utils.xbmc_helper as helper
from bs4 import BeautifulSoup
from utils.mozie_request import Request


class Parser:
    def get(self, response, referrer_url, skipEps=False):
        req = Request()
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        # soup = BeautifulSoup(response, "html.parser")
        # get captcha key
        captcha_key = re.search(r"var recaptcha_key='(.*?)';", response).group(1)
        respon = req.get('https://www.google.com/recaptcha/api2/anchor', params={
            "ar": 1,
            "k": captcha_key,
            "co": "aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbTo0NDM.",
            # "hl": "en",
            "v": "eWmgPeIYKJsH2R2FrgakEIkq",
            "size": "invisible",
            # "cb": "fo0mghgojurx",
        })

        token = re.search('id="recaptcha-token" value="(.*?)"', respon).group(1)
        m_id = re.search(r'id="watch" data-id="(.*?)"', response).group(1)
        ep_id = re.search(r'data-epid="(.*?)"', response).group(1)
        respon = req.get('https://fmovies.to/ajax/film/servers', params={
            'id': m_id,
            'episode': ep_id,
            'token': token
        })
        helper.log(respon)
        return movie

    def get_link(self, response, domain, referrer_url, request):
        helper.log("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # get server list
        soup = BeautifulSoup(response, "html.parser")

        return movie
