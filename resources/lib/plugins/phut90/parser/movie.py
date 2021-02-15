# -*- coding: utf-8 -*-
import re, json
from bs4 import BeautifulSoup


class Parser:

    def get(self, response, url):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        soup = BeautifulSoup(response, "html.parser")

        # get episode if possible
        episodes = soup.select('ul.live-nav-links > li.item > a')
        found = False
        if len(episodes) > 1:
            for episode in episodes:
                if 'javascript' in episode.get('href') or 'dangky' in episode.get('href'):
                    continue
                else:
                    found = True
                    movie['links'].append({
                        'link': "%s%s" % (url, episode.get('href')),
                        'title': episode.text.strip().encode("utf-8"),
                        'type': 'Unknown',
                        'originUrl': url,
                        'resolve': False
                    })

        if not found:
            movie['links'].append({
                'link': url,
                'title': 'Direct link',
                'type': 'Unknown',
                'resolve': False,
                'originUrl': url
            })

        return movie

    def get_link(self, response, originUrl):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.search(r'sources:\s?(.*?),', response)
        print "******************************************************************"
        if sources:
            sources = json.loads(sources.group(1).replace('}],', '}]'))
            try:
                sources = sorted(sources, key=lambda elem: int(elem['label'][0:-1]), reverse=True)
            except:
                pass

            if len(sources) > 0:
                for source in sources:
                    label = 'label' in source and source['label'] or ''
                    movie['links'].append({
                        'link': self.parse_link(source['file']).strip(),
                        'title': 'Link %s' % label.encode('utf-8'),
                        'type': label.encode('utf-8'),
                        'resolve': False,
                        'originUrl': originUrl
                    })
            return movie

        return movie
