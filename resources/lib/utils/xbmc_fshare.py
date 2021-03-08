# -*- coding: utf-8 -*-
import json

from kodi_six import xbmcplugin, xbmcgui, xbmc

from . import xbmc_helper as helper
from .hosts.fshare import FShareVN as Fshare
from .. import app

plugin = app.plugin


class FshareHandler:
    @staticmethod
    def show_fshare_folder():
        query = json.loads(plugin.args['query'][0])
        movie_item = query.get('movie_item')
        item = query.get('item')
        page = query.get('page') or 1
        code = query.get('code')

        if code:
            fshare_items, last_page = Fshare().handleFolder(code=query.get('code'), page=page)
        else:
            fshare_items, last_page = Fshare().handleFolder(query.get('item').get('link'), page=page)

        if not fshare_items: return

        for fshare_item in fshare_items:
            li = xbmcgui.ListItem(label=fshare_item[0])
            is_folder = False
            if fshare_item[1].get('type') == 1:
                li.setInfo('video', {'title': fshare_item[0], 'plot': fshare_item[0]})
                item['link'] = 'https://www.fshare.vn/file/{}'.format(fshare_item[1].get('linkcode'))
                url = plugin.url_for(app.play, query=json.dumps({
                    'item': item, 'movie_item': movie_item, 'direct': 1
                }))
                li.setProperty("IsPlayable", "true")
            else:
                is_folder = True
                url = plugin.url_for(app.show_fshare_folder, query=json.dumps({
                    'item': item, 'movie_item': movie_item, 'code': fshare_item[1].get('linkcode')
                }))
                li.setProperty("IsPlayable", "false")
            xbmcplugin.addDirectoryItem(plugin.handle, url, li, isFolder=is_folder)

        # show next page
        if page < last_page:
            label = "Next page %d / %d >>" % (page, last_page)
            next_item = xbmcgui.ListItem(label=label)

            url = plugin.url_for(app.show_fshare_folder, query=json.dumps({
                'item': item, 'movie_item': movie_item, 'code': code, 'page': page + 1
            }))
            xbmcplugin.addDirectoryItem(plugin.handle, url, next_item, True)

        xbmcplugin.endOfDirectory(plugin.handle)

    @staticmethod
    def play_with_fshare_code():
        xbmcplugin.setPluginCategory(plugin.handle, 'Fshare Code')

        list_item = xbmcgui.ListItem(
            label="Enter code: https://fshare.vn/file/[COLOR orange][B]%s[/B][/COLOR]" % "XXXXXXXXXX",
        )
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(app.playing_with_fshare_code), list_item, isFolder=True)

        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(app.clear_with_fshare_code),
                                    xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear all..."), True)

        # Support to save search history
        items: dict = helper.get_last_fshare_movie()
        for item in items.values():
            url = plugin.url_for(app.play, query=json.dumps({'item': item, 'direct': 1}))
            txt = '[%s] %s' % (item.get('size'), item.get('title'))
            list_item = xbmcgui.ListItem(label=txt)

            if item.get('is_folder') == True:
                url = plugin.url_for(app.show_fshare_folder, query=json.dumps({
                    'item': item, 'movie_item': item
                }))
                list_item.setProperty("IsPlayable", "false")
                xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, True)
            else:
                list_item.setProperty("IsPlayable", "true")
                list_item.setInfo('video', {'title': item.get('title')})
                xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, False)

        xbmcplugin.endOfDirectory(plugin.handle)

    @staticmethod
    def playing_with_fshare_code():
        text = None
        if not plugin.args:
            keyboard = xbmc.Keyboard('', 'Input fshare code:')
            keyboard.doModal()
            if keyboard.isConfirmed():
                text = keyboard.getText()
        else:
            text = plugin.args.get('query')[0]

        if not text:
            return

        url = 'https://fshare.vn/file/{}'.format(text.strip().upper())
        is_folder = False
        try:
            title, size = Fshare.get_info(url=url)
        except:
            is_folder = True

        if is_folder:
            url = 'https://fshare.vn/folder/{}'.format(text.strip().upper())
            try:
                Fshare.get_info(url=url)
                title = url; size = 'Folder'
            except:
                return

        movie = {
            'resolve': False, 'link': url, 'title': title, 'realtitle': title, 'size': size, 'is_folder': is_folder
        }
        helper.save_last_fshare_movie(movie)
        return

    @staticmethod
    def clear_with_fshare_code():
        helper.clear_last_fshare_movie()
