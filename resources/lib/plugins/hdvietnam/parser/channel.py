# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import AsyncRequest
import utils.xbmc_helper as helper


class Parser:
    def get(self, response, page=1, domain=''):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        last_page = soup.select_one('div.PageNav')
        print("*********************** Get pages ")
        if last_page is not None:
            channel['page'] = int(last_page.get('data-last'))

        jobs = []

        for movie in soup.select('li.discussionListItem'):
            # if 'sticky' in movie.get('class'): continue
            tag = movie.select_one('div.listBlock.main a.PreviewTooltip')
            try:
                title = tag.text.strip().encode("utf-8")
                thumb = None

                movie = {
                    'id': tag.get('href'),
                    'label': title,
                    'title': title,
                    'intro': title,
                    'realtitle': title,
                    'thumb': thumb,
                    'type': None
                }

                if 'true' in helper.getSetting('hdvietnam.extra'):
                    jobs.append({
                        'url': '%s/%s' % (domain, movie['id']),
                        'parser': Parser.parse_post,
                        'args': movie
                    })
                else:
                    channel['movies'].append(movie)
            except:
                print(tag)

        if 'true' in helper.getSetting('hdvietnam.extra'):
            channel['movies'] = AsyncRequest(thread=10).get(jobs)
        return channel

    @staticmethod
    def parse_post(response, movie):
        soup = BeautifulSoup(response, "html.parser")
        content = soup.select_one('div.messageContent > article > blockquote.messageText')
        try:
            movie['thumb'] = content.select_one('img.bbCodeImage').get('src')
        except: pass

        return movie

    def get_search(self, response, page=1):

        channel = {
            'page': page,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        last_page = soup.select_one('div.PageNav')
        print("*********************** Get pages ")
        if last_page is not None:
            channel['page'] = int(last_page.get('data-last'))

        for movie in soup.select('li.searchResult'):
            tag = movie.select_one('div.listBlock.main div.titleText > h3.title > a')
            title = tag.text.strip().encode("utf-8")
            thumb = None

            channel['movies'].append({
                'id': tag.get('href'),
                'label': title,
                'title': title,
                'realtitle': title,
                'thumb': thumb,
                'type': None
            })

        return channel
