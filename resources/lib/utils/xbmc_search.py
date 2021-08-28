# -*- coding: utf-8 -*-
import json
from threading import Thread

from kodi_six import xbmcplugin, xbmcgui, xbmc

from . import xbmc_helper as helper
from .. import app
from ..sites import SITES


class Search:
    @staticmethod
    def global_search():
        xbmcplugin.setPluginCategory(app.plugin.handle, 'Search All')

        xbmcplugin.addDirectoryItem(app.plugin.handle,
                                    app.plugin.url_for(app.searching_all),
                                    xbmcgui.ListItem(label="[COLOR orange][B]%s[/B][/COLOR]" % "Enter search text ..."),
                                    True)

        # Support to save search history
        contents = helper.search_history_get()
        if contents:
            xbmcplugin.addDirectoryItem(app.plugin.handle,
                                        app.plugin.url_for(app.clear_search),
                                        xbmcgui.ListItem(
                                            label="[COLOR red][B]%s[/B][/COLOR]" % "Clear search text ..."),
                                        True)
            for txt in contents:
                xbmcplugin.addDirectoryItem(app.plugin.handle,
                                            app.plugin.url_for(app.searching_all, query=txt),
                                            xbmcgui.ListItem(label="[COLOR blue][B]%s[/B][/COLOR]" % txt), True)

        xbmcplugin.endOfDirectory(app.plugin.handle)

    @staticmethod
    def searching_all():
        text = None
        if not app.plugin.args:
            keyboard = xbmc.Keyboard('', 'Search iPlayer')
            keyboard.doModal()
            if keyboard.isConfirmed():
                text = keyboard.getText()
        else:
            text = app.plugin.args.get('query')[0]

        if not text:
            return

        xbmcplugin.setPluginCategory(app.plugin.handle, 'Search Result: {}'.format(text))
        xbmcplugin.setContent(app.plugin.handle, 'movies')

        helper.search_history_save(text)
        progress = {
            'percent': 0,
            'step': 5,
            'counter': 0,
            'length': 0,
            'dialog': xbmcgui.DialogProgress(),
            'results': []
        }

        def _search(site, text, progress):
            try:
                plugin, module, class_name = app.load_plugin(
                    {'className': site.get('className'), "module": site.get('plugin')})
                progress['dialog'].update(
                    int(progress['percent']),
                    'Searching on %s totally %d/%d sites' % (class_name, progress['counter'], progress['length']))

                progress['results'].append((module, class_name, plugin().search(text)))
                progress['percent'] += progress['step']
                progress['counter'] += 1
                progress['dialog'].update(
                    int(progress['percent']),
                    'Searching on %s totally %d/%d sites' % (class_name, progress['counter'], progress['length']))

            except Exception as inst:
                helper.log(type(inst))
                helper.log(inst.args)
                helper.log(inst)
                pass

        threads = []

        sites = SITES
        for group in sites:
            if group['version'] > helper.KODI_VERSION or ('searchable' in group and not group['searchable']):
                continue
            for site in group['sites']:
                progress['length'] += 1
                progress['dialog'].create('Processing',
                                          "Searching %d/%d sites" % (progress['counter'], progress['length']))
                progress['step'] = 100 / progress['length']

        for group in sites:
            if group['version'] > helper.KODI_VERSION or ('searchable' in group and not group['searchable']):
                continue
            for site in group['sites']:
                if site['version'] > helper.KODI_VERSION or ('searchable' in site and not site['searchable']):
                    continue
                process = Thread(target=_search, args=[site, text, progress])
                process.setDaemon(True)
                process.start()
                threads.append(process)

        for process in threads:
            process.join()

        for module, class_name, movies in progress['results']:
            # if movies is not None and len(movies.get('movies')) > 0:
            label = "[COLOR red][B][---- %s : [COLOR yellow]%d found[/COLOR] View All ----][/B][/COLOR]" % (
                class_name, len(movies['movies']))
            sli = xbmcgui.ListItem(label=label)

            url = app.plugin.url_for(app.searching,
                                     query=json.dumps({'module': module, 'className': class_name, 'text': text}))
            xbmcplugin.addDirectoryItem(app.plugin.handle, url, sli, isFolder=True)

            for item in movies['movies'][:5]:
                try:
                    list_item = xbmcgui.ListItem(label=item['label'])
                    list_item.setLabel2(item['realtitle'])
                    list_item.setArt({
                        'thumb': item['thumb'],
                    })

                    url = app.plugin.url_for(app.show_movie, query=json.dumps({
                        'movie_item': item, 'cat_name': 'Search',
                        'module': module, 'className': class_name
                    }))
                    xbmcplugin.addDirectoryItem(app.plugin.handle, url, list_item, isFolder=True)
                except:
                    helper.log(item)
        xbmcplugin.endOfDirectory(app.plugin.handle)

    @staticmethod
    def search():
        query = json.loads(app.plugin.args['query'][0])
        instance, module, class_name = app.load_plugin(query)

        xbmcplugin.setPluginCategory(app.plugin.handle, 'Search')
        url = app.plugin.url_for(app.searching, query=json.dumps({'module': module, 'className': class_name}))

        xbmcplugin.addDirectoryItem(app.plugin.handle, url,
                                    xbmcgui.ListItem(label="[COLOR orange][B]%s[/B][/COLOR]" % "Enter search text ..."),
                                    True)

        # Support to save search history
        contents = helper.search_history_get()
        if contents:
            xbmcplugin.addDirectoryItem(app.plugin.handle, app.plugin.url_for(app.clear_search),
                                        xbmcgui.ListItem(
                                            label="[COLOR red][B]%s[/B][/COLOR]" % "Clear search text ..."),
                                        True)
            for txt in contents:
                try:
                    url = app.plugin.url_for(app.searching,
                                             query=json.dumps({'module': module, 'className': class_name, 'text': txt}))
                    xbmcplugin.addDirectoryItem(app.plugin.handle, url,
                                                xbmcgui.ListItem(label="[COLOR blue][B]%s[/B][/COLOR]" % txt), True)
                except:
                    pass
        xbmcplugin.endOfDirectory(app.plugin.handle)

    @staticmethod
    def searching():
        query = json.loads(app.plugin.args['query'][0])
        instance, module, class_name = app.load_plugin(query)
        text = query.get('text')

        xbmcplugin.setPluginCategory(app.plugin.handle, 'Search / %s' % text)
        xbmcplugin.setContent(app.plugin.handle, 'movies')
        if not text:
            keyboard = xbmc.Keyboard('', 'Search iPlayer')
            keyboard.doModal()
            if keyboard.isConfirmed():
                text = keyboard.getText()

        if not text:
            return

        helper.search_history_save(text)
        movies = instance().search(text)

        if movies is not None:
            label = "[COLOR red][B][---- %s : [COLOR yellow]%d found[/COLOR] View All ----][/B][/COLOR]" % (
                class_name, len(movies['movies']))
            sli = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(app.plugin.handle, None, sli, isFolder=False)

            for item in movies['movies']:
                try:
                    list_item = xbmcgui.ListItem(label=item['label'])
                    list_item.setLabel2(item['realtitle'])
                    list_item.setArt({
                        'thumb': item['thumb'],
                    })
                    url = app.plugin.url_for(app.show_movie, query=json.dumps({
                        'movie_item': item, 'cat_name': 'Search',
                        'module': module, 'className': class_name
                    }))
                    xbmcplugin.addDirectoryItem(app.plugin.handle, url, list_item, isFolder=True)
                except:
                    helper.log(item)
        else:
            return

        xbmcplugin.endOfDirectory(app.plugin.handle)

    @staticmethod
    def clear_search():
        helper.search_history_clear()
        return

    @staticmethod
    def show_last_watched():
        items: dict = helper.get_last_watch_movie()
        if items:
            xbmcplugin.addDirectoryItem(app.plugin.handle, app.plugin.url_for(app.clear_last_watched),
                                        xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear list ..."), True)
            for item in items.values():
                movie = item.get('movie_item')
                list_item = xbmcgui.ListItem(label=movie.get('label'))
                list_item.addContextMenuItems(app.globalContextMenu())
                list_item.setLabel2(movie.get('realtitle'))
                list_item.setArt({'thumb': movie.get('thumb')})
                if 'poster' in movie:
                    list_item.setArt({'poster': movie.get('poster')})
                if 'intro' in movie:
                    list_item.setInfo(type='video', infoLabels={'plot': movie.get('intro')})

                url = app.plugin.url_for(app.show_movie, query=json.dumps({
                    'movie_item': movie, 'cat_name': 'Watching',
                    'module': item.get('module'), 'className': item.get('className')
                }))
                xbmcplugin.addDirectoryItem(app.plugin.handle, url, list_item, isFolder=True)

        xbmcplugin.endOfDirectory(app.plugin.handle)

    @staticmethod
    def clear_last_watched():
        helper.clear_last_watch_movie()
        return
