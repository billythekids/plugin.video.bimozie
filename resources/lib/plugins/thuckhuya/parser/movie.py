# -*- coding: utf-8 -*-
import json
import re


class Parser:

    def get(self, response, url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        response = re.search(r'detail\((.*)\)', response)

        response = json.loads(response.group(1))
        for k, v in response.get('data').get('stream').items():
            movie['links'].append({
                'link': v,
                'title': k.upper(),
                'type': 'Unknown',
                'resolve': False
            })

        # soup = BeautifulSoup(response, "html.parser")
        #
        # # get episode if possible
        # episodes = soup.select('#play_main a.text-uppercase.action ')
        # found = False
        # if len(episodes) > 1:
        #     for episode in episodes:
        #         if 'javascript' in episode.get('href') or 'dangky' in episode.get('href'):
        #             continue
        #         else:
        #             found = True
        #             movie['links'].append({
        #                 'link': episode.get('href'),
        #                 'title': py2_encode(episode.text.strip()),
        #                 'type': 'Unknown',
        #                 'originUrl': 'https://mitom1.tv/',
        #                 'resolve': False
        #             })
        #
        # if not found:
        #     movie['links'].append({
        #         'link': url,
        #         'title': 'Direct link',
        #         'type': 'Unknown',
        #         'resolve': False,
        #         'originUrl': 'https://play.thuckhuya.live/'
        #     })

        return movie
