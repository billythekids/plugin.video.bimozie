#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class Parser:
    def get(self, response, page, domain="http://fimfast.tv"):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }
        soup = BeautifulSoup(response, "html.parser")

        pages = soup.select('ul.page-numbers > li')
        if len(pages) > 2:
            channel['page'] = int(pages[-2].select_one('a').find(text=True, recursive=True))

        for movie in soup.select('article.grid-item'):
            movie = movie.select_one('> div.halim-item > a')
            title = movie.select_one('div.halim-post-title-box h2.entry-title').text.encode("utf-8")
            real_title = movie.select_one('div.halim-post-title-box p.original_title').text.encode("utf-8")
            quality = movie.select_one('span.status')

            if quality:
                quality = quality.text.encode("utf-8")

            label = "[{}] {}".format(quality, title)
            thumb = "{}/{}".format(domain, movie.select_one('figure > img.lazyload').get('data-src'))

            total_eps = movie.select_one('span.episode')
            if total_eps:
                total_eps = total_eps.text.strip().encode("utf-8")
                label = "[{} {}] {}".format(total_eps, quality, title)

            channel['movies'].append({
                'id': movie.get('href'),
                'label': label,
                'title': title,
                'realtitle': real_title,
                'thumb': thumb,
                'poster': thumb,
                'type': quality
            })

        return channel
