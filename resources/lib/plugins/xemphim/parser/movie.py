# -*- coding: utf-8 -*-
import re
import json


class Parser:
    def get(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        m = json.loads(response)['data']['title']
        # subtitle
        subtitle = ""
        for sub in m['subtitles']:
            subtitle = 'https://b.xemphim.plus/subtitles/{}-{}.vtt'.format(sub['hash'], sub['updatedAt'])
            if 'vi' in sub['language']:
                break

        movie['links'].append({
            'link': m['srcUrl'],
            'title': 'Link direct',
            'type': 'mp4',
            'subtitle': subtitle,
            'resolve': False,
            'originUrl': 'https://xemphim.plus'
        })

        return movie

