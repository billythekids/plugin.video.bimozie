# -*- coding: utf-8 -*-
import json

from kodi_six import xbmcplugin, xbmcgui

from . import xbmc_helper as helper
from .. import app
from ..sites import SITES

plugin = app.plugin


class SiteHandler:
    @staticmethod
    def index():
        xbmcplugin.setPluginCategory(plugin.handle, 'Websites')

        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(app.show_last_watched),
                                    xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Last Watched..."),
                                    True)

        for idx, site in enumerate(SITES):
            if site['version'] > helper.KODI_VERSION:
                helper.log("***********************Skip version %d" % site['version'])
                continue

            list_item = xbmcgui.ListItem(label=site['name'])
            list_item.addContextMenuItems(app.globalContextMenu())
            list_item.setArt({'thumb': site['logo'], 'icon': site['logo']})
            url = plugin.url_for(app.show_site_group, idx)

            xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

        xbmcplugin.endOfDirectory(plugin.handle, cacheToDisc=True)

    @staticmethod
    def show_site_group(group_index):
        xbmcplugin.setPluginCategory(plugin.handle, 'Websites')

        group_index = int(group_index)
        sites = SITES

        if sites[group_index]['searchable']:
            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(app.global_search),
                                        xbmcgui.ListItem(label="[COLOR yellow][B] %s [/B][/COLOR]" % "Search All..."),
                                        True)

        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(app.show_last_watched),
                                    xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Last Watched..."),
                                    True)

        if 'fshare' in sites[group_index].get('name').lower():
            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(app.play_with_fshare_code),
                                        xbmcgui.ListItem(
                                            label="[COLOR blue][B] %s [/B][/COLOR]" % "Play direct with fshare code..."),
                                        True)

        for site in sites[group_index]['sites']:
            if site['version'] > helper.KODI_VERSION:
                helper.log("***********************Skip version %s" % site['name'])
                continue

            list_item = xbmcgui.ListItem(label=site['name'])
            list_item.addContextMenuItems(app.globalContextMenu())
            list_item.setArt({'thumb': site['logo'], 'icon': site['logo']})
            url = plugin.url_for(app.show_site_category,
                                 query=json.dumps({'searchable': site.get('searchable'), 'module': site['plugin'],
                                                   'className': site['className']}))

            xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

        xbmcplugin.endOfDirectory(plugin.handle, cacheToDisc=True)

    @staticmethod
    def show_site_category():
        query = json.loads(plugin.args['query'][0])
        instance, module, class_name = app.load_plugin(query)
        cats, movies = instance().getCategory()
        xbmcplugin.setPluginCategory(plugin.handle, class_name)
        searchable: bool = query.get('searchable')

        # show search link
        if searchable != False:
            url = plugin.url_for(app.search, query=json.dumps({'module': module, 'className': class_name}))
            xbmcplugin.addDirectoryItem(plugin.handle, url,
                                        xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Search..."), True)

        # Show category
        for cat in cats:
            list_item = xbmcgui.ListItem(label=cat.get('title'))
            list_item.addContextMenuItems(app.globalContextMenu())
            if 'subcategory' in cat and len(cat.get('subcategory')) > 0:
                url = plugin.url_for(app.show_site_subcategory, query=json.dumps({
                    'url': cat.get('link'), 'name': cat.get('title'),
                    'subcategory': cat.get('subcategory'),
                    'module': module, 'className': class_name
                }))

            else:
                url = plugin.url_for(app.show_movies, query=json.dumps({
                    'url': cat.get('link'), 'name': cat.get('title'), 'page': 1,
                    'module': module, 'className': class_name
                }))
            xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

        if movies and len(movies) > 0:
            if len(cats) > 0:
                label = "[COLOR yellow][B][---- New Movies ----][/B][/COLOR]"
                sli = xbmcgui.ListItem(label=label)
                xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)

            app.show_movies(movies, '/', 1, '', module, class_name)
        else:
            xbmcplugin.endOfDirectory(plugin.handle)

    @staticmethod
    def show_site_subcategory():
        xbmcplugin.setContent(plugin.handle, 'files')
        query = json.loads(plugin.args['query'][0])
        instance, module, class_name = app.load_plugin(query)
        xbmcplugin.setPluginCategory(plugin.handle, '{} / {}'.format(class_name, query.get('name')))

        for cat in query.get('subcategory'):
            list_item = xbmcgui.ListItem(label=cat.get('title'))
            list_item.addContextMenuItems(app.globalContextMenu())
            url = plugin.url_for(app.show_movies, query=json.dumps({
                'url': cat.get('link'), 'page': 1, 'name': '{} - {}'.format(query.get('name'), cat.get('title')),
                'module': module, 'className': class_name
            }))
            xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)
        xbmcplugin.endOfDirectory(plugin.handle)
