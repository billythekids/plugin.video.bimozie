# -*- coding: latin1 -*-
from bs4 import BeautifulSoup


class Parser:
    def get(self, response, referrer_url, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get server group and link
        servers = soup.select('div.server.server-group')

        return movie

    def get_link(self, response, domain, referrer_url, request):
        print("***********************Get Movie Link*****************************")
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        # get server list
        soup = BeautifulSoup(response, "html.parser")

        return movie
