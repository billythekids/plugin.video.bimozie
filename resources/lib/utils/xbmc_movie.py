# -*- coding: utf-8 -*-
import json

from kodi_six import xbmcplugin, xbmcgui

from . import xbmc_helper as helper
from .. import app

plugin = app.plugin


def _build_ep_list(items, movie_item, module, class_name):
    thumb = helper.text_encode(movie_item.get('thumb'))
    title = helper.text_encode(movie_item.get('realtitle'))

    for item in items:
        try:
            li = xbmcgui.ListItem(label=item['title'])
            li.setInfo('video', {'title': item['title']})
            if item.get('thumb'): thumb = item.get('thumb')
            li.setProperty('fanart_image', thumb)
            li.setArt({'thumb': thumb})
            li.setInfo(type='video', infoLabels={'plot': movie_item.get('intro')})
            li.setLabel2(title)
            if 'intro' in item:
                li.setInfo(type='video', infoLabels={'plot': item['intro']})
            else:
                li.setInfo(type='video', infoLabels={'plot': item['title']})

            eps_title = helper.text_encode(item.get('title'))
            movie_item['title'] = "%s - %s" % (title, eps_title)

            url = plugin.url_for(app.play, query=json.dumps({
                'item': item, 'movie_item': movie_item, 'direct': 0,
                'module': module, 'className': class_name
            }))
            li.setProperty("IsPlayable", "true")
            xbmcplugin.addDirectoryItem(plugin.handle, url, li, isFolder=False)
        except:
            helper.log(items)


class MovieHandler:
    @staticmethod
    def show_movies(movies=None, link=None, page=0, cat_name="", module=None, class_name=None):
        if not movies:
            query = json.loads(plugin.args['query'][0])
            instance, module, class_name = app.load_plugin(query)
            xbmcplugin.setPluginCategory(plugin.handle, '{} / {}'.format(class_name, query.get('name')))

            link, page, cat_name = query.get('url'), int(query.get('page')), query.get('name')
            movies = instance().getChannel(link, page)

        if movies is not None:
            for item in movies.get('movies'):
                try:
                    list_item = xbmcgui.ListItem(label=item.get('label'))
                    list_item.addContextMenuItems(app.globalContextMenu())
                    list_item.setLabel2(item.get('realtitle'))
                    list_item.setArt({'thumb': item['thumb']})
                    if 'poster' in item:
                        list_item.setArt({'poster': item['poster']})
                    if 'intro' in item:
                        list_item.setInfo(type='video', infoLabels={'plot': item['intro']})

                    if item.get('type') == 'Fshare':
                        is_folder = item.get('isFolder') and True or False
                        if is_folder:
                            url = plugin.url_for(app.show_fshare_folder, query=json.dumps({
                                'item': item, 'movie_item': item, 'code': item.get('code')
                            }))
                        else:
                            list_item.setInfo('video', {'title': item.get('title')})
                            url = plugin.url_for(app.play, query=json.dumps({
                                'item': item, 'movie_item': item, 'direct': 1
                            }))
                            list_item.setProperty("IsPlayable", "true")
                    else:
                        is_folder = True
                        url = plugin.url_for(app.show_movie, query=json.dumps({
                            'movie_item': item, 'cat_name': cat_name,
                            'module': module, 'className': class_name
                        }))

                    xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=is_folder)
                except Exception as inst:
                    helper.log("*********************** List Movie Exception: {}".format(inst))
                    helper.log(item)

            # show next page
            if movies['page'] > 1 and page < movies['page']:
                label = "Next page %d / %d >>" % (page, movies['page'])
                next_item = xbmcgui.ListItem(label=label)
                if 'page_patten' in movies and movies['page_patten'] is not None:
                    link = movies['page_patten']

                url = plugin.url_for(app.show_movies, query=json.dumps({
                    'url': link, 'page': int(page) + 1,
                    'module': module, 'className': class_name
                }))
                xbmcplugin.addDirectoryItem(plugin.handle, url, next_item, True)

        xbmcplugin.endOfDirectory(plugin.handle)

    @staticmethod
    def show_movie():
        query = json.loads(plugin.args['query'][0])
        instance, module, class_name = app.load_plugin(query)

        movie_item = query.get('movie_item')
        movie = instance().getMovie(movie_item.get('id'))

        xbmcplugin.setPluginCategory(plugin.handle,
                                     '{} / {} / {}'.format(class_name, query.get('cat_name'), movie_item.get('title')))
        xbmcplugin.setContent(plugin.handle, 'movies')

        if len(movie['group']) > 0:
            helper.log("*********************** Display movie episode/group")
            idx = 0
            for key in movie.get('group'):
                items = movie.get('group').get(key)
                idx += 1
                label = "[COLOR red][B][---- %s : [COLOR yellow]%d eps[/COLOR] ----][/B][/COLOR]" % (key, len(items))
                sli = xbmcgui.ListItem(label=label)

                if len(items) < 5 or len(movie['group']) < 1:
                    xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)
                    _build_ep_list(items, movie_item, module, class_name)

                elif idx is len(movie['group']):
                    xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)
                    _build_ep_list(items, movie_item, module, class_name)

                else:
                    url = plugin.url_for(app.show_movie_server_group, query=json.dumps({
                        'server': key, 'items': items, 'movie_item': movie_item,
                        'module': module, 'className': class_name
                    }))
                    xbmcplugin.addDirectoryItem(plugin.handle, url, sli, isFolder=True)

        else:
            helper.log("*********************** Display movie links")
            thumb = movie_item.get('thumb')
            for item in movie['links']:

                li = xbmcgui.ListItem(label=item['title'])
                li.setInfo('video', {'title': item['title']})
                li.setProperty('fanart_image', thumb)
                li.setArt({'thumb': thumb})
                if 'intro' in item:
                    li.setInfo(type='video', infoLabels={'plot': item['intro']})

                if 'isFolder' in item and item.get('isFolder') and 'fshare' in item.get('link'):
                    url = plugin.url_for(app.show_fshare_folder, query=json.dumps({
                        'item': item, 'movie_item': movie_item
                    }))
                    li.setProperty("IsPlayable", "false")
                    xbmcplugin.addDirectoryItem(plugin.handle, url, li, True)
                else:
                    url = plugin.url_for(app.play, query=json.dumps({
                        'item': item, 'movie_item': movie_item, 'direct': 1,
                        'module': module, 'className': class_name
                    }))
                    li.setProperty("IsPlayable", "true")
                    xbmcplugin.addDirectoryItem(plugin.handle, url, li, False)

        # save watching movie
        if 'Phut90' not in class_name and 'Thuckhuya' not in class_name:
            helper.save_last_watch_movie(query)
        xbmcplugin.endOfDirectory(plugin.handle)

    @staticmethod
    def show_movie_server_group():
        query = json.loads(plugin.args['query'][0])
        instance, module, class_name = app.load_plugin(query)

        xbmcplugin.setContent(plugin.handle, 'movies')
        xbmcplugin.setPluginCategory(plugin.handle,
                                     "%s - %s " % (query.get('movie_item').get('title'), query.get('server')))

        label = "[COLOR red][B][---- %s : [COLOR yellow]%d eps[/COLOR] ----][/B][/COLOR]" % (
            query.get('server'), len(query.get('items'))
        )
        sli = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)
        _build_ep_list(query.get('items'), query.get('movie_item'), module, class_name)
        xbmcplugin.endOfDirectory(plugin.handle)
