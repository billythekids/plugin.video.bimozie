# -*- coding: utf-8 -*-
import json
import re
from collections import OrderedDict
from importlib import import_module
from threading import Thread

import routing
import utils.xbmc_helper as helper
# from kodi_six import xbmcplugin, xbmcgui, xbmc
import xbmc
import xbmcgui
import xbmcplugin
from kodi_six.utils import py2_encode
from utils.hosts.fshare import FShareVN as Fshare
from utils.media_helper import MediaHelper

plugin = routing.Plugin()


def globalContextMenu():
    commands = list()
    commands.append(('Settings', 'Addon.OpenSettings(%s)' % helper.ADDON_ID,))
    return commands


@plugin.route('/')
def index():
    xbmcplugin.setPluginCategory(plugin.handle, 'Websites')

    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_last_watched),
                                xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Last Watched..."), True)

    for idx, site in enumerate(helper.get_sites_config()):
        if site['version'] > helper.KODI_VERSION:
            print("***********************Skip version %d" % site['version'])
            continue

        list_item = xbmcgui.ListItem(label=site['name'])
        list_item.addContextMenuItems(globalContextMenu())
        list_item.setArt({'thumb': site['logo'], 'icon': site['logo']})
        url = plugin.url_for(show_site_group, idx)

        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(plugin.handle, cacheToDisc=True)


@plugin.route('/group/<group_index>')
def show_site_group(group_index):
    xbmcplugin.setPluginCategory(plugin.handle, 'Websites')

    group_index = int(group_index)
    sites = helper.get_sites_config()

    if sites[group_index]['searchable']:
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(global_search),
                                    xbmcgui.ListItem(label="[COLOR yellow][B] %s [/B][/COLOR]" % "Search All..."), True)

    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(show_last_watched),
                                xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Last Watched..."), True)

    for site in sites[group_index]['sites']:
        if site['version'] > helper.KODI_VERSION:
            print("***********************Skip version %s" % site['name'])
            continue

        list_item = xbmcgui.ListItem(label=site['name'])
        list_item.addContextMenuItems(globalContextMenu())
        list_item.setArt({'thumb': site['logo'], 'icon': site['logo']})
        url = plugin.url_for(show_site_category,
                             query=json.dumps({'searchable': site.get('searchable'), 'module': site['plugin'],
                                               'className': site['className']}))

        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(plugin.handle, cacheToDisc=True)


@plugin.route('/category')
def show_site_category():
    query = json.loads(plugin.args['query'][0])
    instance, module, class_name = load_plugin(query)
    cats, movies = instance().getCategory()
    xbmcplugin.setPluginCategory(plugin.handle, class_name)
    searchable: bool = query.get('searchable')

    # show search link
    if searchable != False:
        url = plugin.url_for(search, query=json.dumps({'module': module, 'className': class_name}))
        xbmcplugin.addDirectoryItem(plugin.handle, url,
                                    xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Search..."), True)

    # Show category
    for cat in cats:
        list_item = xbmcgui.ListItem(label=cat['title'])
        list_item.addContextMenuItems(globalContextMenu())
        if 'subcategory' in cat and len(cat['subcategory']) > 0:
            url = plugin.url_for(show_site_subcategory, query=json.dumps({
                'url': cat.get('link'), 'name': cat['title'],
                'subcategory': cat['subcategory'],
                'module': module, 'className': class_name
            }))

        else:
            url = plugin.url_for(show_movies, query=json.dumps({
                'url': cat.get('link'), 'name': cat.get('title'), 'page': 1,
                'module': module, 'className': class_name
            }))
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

    if movies and len(movies) > 0:
        if len(cats) > 0:
            label = "[COLOR yellow][B][---- New Movies ----][/B][/COLOR]"
            sli = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)
        show_movies(movies, '/', 1, '', module, class_name)
    else:
        xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/subcategory')
def show_site_subcategory():
    query = json.loads(plugin.args['query'][0])
    instance, module, class_name = load_plugin(query)
    xbmcplugin.setPluginCategory(plugin.handle, '{} / {}'.format(class_name, query.get('name')))

    for cat in query.get('subcategory'):
        list_item = xbmcgui.ListItem(label=cat.get('title'))
        list_item.addContextMenuItems(globalContextMenu())
        url = plugin.url_for(show_movies, query=json.dumps({
            'url': cat.get('link'), 'page': 1, 'name': '{} - {}'.format(query.get('name'), cat.get('title')),
            'module': module, 'className': class_name
        }))
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/movies')
def show_movies(movies=None, link=None, page=0, cat_name="", module=None, class_name=None):
    if not movies:
        query = json.loads(plugin.args['query'][0])
        instance, module, class_name = load_plugin(query)
        xbmcplugin.setPluginCategory(plugin.handle, '{} / {}'.format(class_name, query.get('name')))

        link, page, cat_name = query.get('url'), int(query.get('page')), query.get('name')
        movies = instance().getChannel(link, page)

    if movies is not None:
        for item in movies.get('movies'):
            try:
                list_item = xbmcgui.ListItem(label=item.get('label'))
                list_item.addContextMenuItems(globalContextMenu())
                list_item.setLabel2(item.get('realtitle'))
                list_item.setArt({'thumb': item['thumb']})
                if 'poster' in item:
                    list_item.setArt({'poster': item['poster']})
                if 'intro' in item:
                    list_item.setInfo(type='video', infoLabels={'plot': item['intro']})

                url = plugin.url_for(show_movie, query=json.dumps({
                    'movie_item': item, 'cat_name': cat_name,
                    'module': module, 'className': class_name
                }))
                xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)
            except Exception as inst:
                print("*********************** List Movie Exception: {}".format(inst))
                print(item)

        # show next page
        if movies['page'] > 1 and page < movies['page']:
            label = "Next page %d / %d >>" % (page, movies['page'])
            next_item = xbmcgui.ListItem(label=label)
            if 'page_patten' in movies and movies['page_patten'] is not None:
                link = movies['page_patten']

            url = plugin.url_for(show_movies, query=json.dumps({
                'url': link, 'page': int(page) + 1,
                'module': module, 'className': class_name
            }))
            xbmcplugin.addDirectoryItem(plugin.handle, url, next_item, True)

    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/movie')
def show_movie():
    query = json.loads(plugin.args['query'][0])
    instance, module, class_name = load_plugin(query)

    movie_item = query.get('movie_item')
    movie = instance().getMovie(movie_item.get('id'))

    xbmcplugin.setPluginCategory(plugin.handle,
                                 '{} / {} / {}'.format(class_name, query.get('cat_name'), movie_item.get('title')))
    xbmcplugin.setContent(plugin.handle, 'movies')

    if len(movie['group']) > 0:
        print("*********************** Display movie episode/group")
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
                url = plugin.url_for(show_movie_server_group, query=json.dumps({
                    'server': key, 'items': items, 'movie_item': movie_item,
                    'module': module, 'className': class_name
                }))
                xbmcplugin.addDirectoryItem(plugin.handle, url, sli, isFolder=True)

    else:
        print("*********************** Display movie links")
        thumb = movie_item.get('thumb')
        for item in movie['links']:

            li = xbmcgui.ListItem(label=item['title'])
            li.setInfo('video', {'title': item['title']})
            li.setProperty('fanart_image', thumb)
            li.setArt({'thumb': thumb})
            if 'intro' in item:
                li.setInfo(type='video', infoLabels={'plot': item['intro']})

            if 'isFolder' in item and item.get('isFolder') and 'fshare' in item.get('link'):
                url = plugin.url_for(show_fshare_folder, query=json.dumps({
                    'item': item, 'movie_item': movie_item
                }))
                li.setProperty("IsPlayable", "false")
                xbmcplugin.addDirectoryItem(plugin.handle, url, li, True)
            else:
                url = plugin.url_for(play, query=json.dumps({
                    'item': item, 'movie_item': movie_item, 'direct': 1,
                    'module': module, 'className': class_name
                }))
                li.setProperty("IsPlayable", "true")
                xbmcplugin.addDirectoryItem(plugin.handle, url, li, False)

    # save watching movie
    if 'Phut90' not in class_name:
        helper.save_last_watch_movie(query)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/movieItemFolder')
def show_fshare_folder():
    query = json.loads(plugin.args['query'][0])
    movie_item = query.get('movie_item')
    item = query.get('item')
    page = query.get('page') or 1
    code = query.get('code')

    if code:
        fshare_items, last_page = Fshare('').handleFolder(code=query.get('code'), page=page)
    else:
        fshare_items, last_page = Fshare('').handleFolder(query.get('item').get('link'), page=page)

    for fshare_item in fshare_items:
        li = xbmcgui.ListItem(label=fshare_item[0])
        is_folder = False
        if fshare_item[1].get('type') == 1:
            li.setInfo('video', {'title': fshare_item[0]})
            item['link'] = 'https://www.fshare.vn/file/{}'.format(fshare_item[1].get('linkcode'))
            url = plugin.url_for(play, query=json.dumps({
                'item': item, 'movie_item': movie_item, 'direct': 1
            }))
            li.setProperty("IsPlayable", "true")
        else:
            is_folder = True
            url = plugin.url_for(show_fshare_folder, query=json.dumps({
                'item': item, 'movie_item': movie_item, 'code': fshare_item[1].get('linkcode')
            }))
            li.setProperty("IsPlayable", "false")
        xbmcplugin.addDirectoryItem(plugin.handle, url, li, isFolder=is_folder)

    # show next page
    if page < last_page:
        label = "Next page %d / %d >>" % (page, last_page)
        next_item = xbmcgui.ListItem(label=label)

        url = plugin.url_for(show_fshare_folder, query=json.dumps({
            'item': item, 'movie_item': movie_item, 'code': code, 'page': page + 1
        }))
        xbmcplugin.addDirectoryItem(plugin.handle, url, next_item, True)

    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/server_group')
def show_movie_server_group():
    query = json.loads(plugin.args['query'][0])
    instance, module, class_name = load_plugin(query)

    xbmcplugin.setPluginCategory(plugin.handle,
                                 "%s - %s " % (query.get('movie_item').get('title'), query.get('server')))

    label = "[COLOR red][B][---- %s : [COLOR yellow]%d eps[/COLOR] ----][/B][/COLOR]" % (
        query.get('server'), len(query.get('items'))
    )
    sli = xbmcgui.ListItem(label=label)
    xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)
    _build_ep_list(query.get('items'), query.get('movie_item'), module, class_name)
    xbmcplugin.endOfDirectory(plugin.handle)


def _build_ep_list(items, movie_item, module, class_name):
    thumb = py2_encode(movie_item.get('thumb'))
    title = py2_encode(movie_item.get('realtitle'))

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

            eps_title = py2_encode(item.get('title'))
            movie_item['title'] = "%s - %s" % (title, eps_title)

            url = plugin.url_for(play, query=json.dumps({
                'item': item, 'movie_item': movie_item, 'direct': 0,
                'module': module, 'className': class_name
            }))
            li.setProperty("IsPlayable", "true")
            xbmcplugin.addDirectoryItem(plugin.handle, url, li, isFolder=False)
        except:
            print(items)


@plugin.route('/play')
def play():
    query = json.loads(plugin.args['query'][0])
    play_item = xbmcgui.ListItem()

    if int(query.get('direct')) == 0:
        instance, module, class_name = load_plugin(query)
        movie_item = query.get('movie_item')
        thumb = py2_encode(movie_item.get('thumb'))
        title = py2_encode(movie_item.get('title'))
        realtitle = py2_encode(movie_item.get('realtitle'))

        movie = instance().getLink(query.get('item'))
        if not movie or 'links' not in movie or len(movie['links']) == 0:
            return
        else:
            blacklist = ['hydrax', 'maya.bbigbunny.ml', 'blob', 'short.icu']

            def filter_blacklist(m):
                for i in blacklist:
                    if i in m['link']: return False
                return True

            movie['links'] = list(filter(filter_blacklist, movie['links']))
            if len(movie['links']) > 1:
                # sort all links
                try:
                    movie['links'] = sorted(
                        movie['links'], key=lambda elem: re.search(r'(\d+)', elem['title'])
                                                         and int(re.search(r'(\d+)', elem['title']).group(1))
                                                         or 0,
                        reverse=True
                    )
                except Exception as e:
                    print(e)

                listitems = []
                appened_list = []
                for i in movie['links']:
                    if not next((d for d in appened_list if i.get('link') == d.get('link')), False):
                        listitems.append("%s (%s)" % (i["title"], i["link"]))
                        appened_list.append(i)

                index = xbmcgui.Dialog().select("Select stream", listitems)
                if index == -1:
                    return None
                else:
                    movie = appened_list[index]
            else:
                movie = movie['links'][0]

            play_item.setArt({'thumb': thumb})
            play_item.setLabel(title)
            play_item.setLabel2(realtitle)
            play_item.setInfo('video', {
                'title': title,
                'originaltitle': realtitle,
                'plot': movie_item.get('intro')
            })
    else:
        movie = query.get('item')

    # Parse link
    mediatype = MediaHelper.resolve_link(movie)

    if not movie['link']: return
    if movie.get('subtitle'):
        if isinstance(movie['subtitle'], list):
            play_item.setSubtitles(movie['subtitle'])
        else:
            play_item.setSubtitles([movie['subtitle']])
    if mediatype == 'inputstream':
        play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        play_item.setContentLookup(False)
        link = movie['link'].split('|')
        if link and len(link) > 1:
            play_item.setProperty('inputstream.adaptive.stream_headers', link[1])

    play_item.setProperty('IsPlayable', 'true')
    play_item.setPath(movie['link'])
    xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)


@plugin.route('/searchAll')
def global_search():
    xbmcplugin.setPluginCategory(plugin.handle, 'Search All')

    xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(searching_all),
                                xbmcgui.ListItem(label="[COLOR orange][B]%s[/B][/COLOR]" % "Enter search text ..."),
                                True)

    # Support to save search history
    contents = helper.search_history_get()
    if contents:
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(clear_search),
                                    xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear search text ..."),
                                    True)
        for txt in contents:
            xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(searching_all, query=txt),
                                        xbmcgui.ListItem(label="[COLOR blue][B]%s[/B][/COLOR]" % txt), True)

    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/searchingAll')
def searching_all():
    text = None
    if not plugin.args:
        keyboard = xbmc.Keyboard('', 'Search iPlayer')
        keyboard.doModal()
        if keyboard.isConfirmed():
            text = keyboard.getText()
    else:
        text = plugin.args.get('query')[0]

    if not text:
        return

    xbmcplugin.setPluginCategory(plugin.handle, 'Search Result: {}'.format(text))
    xbmcplugin.setContent(plugin.handle, 'movies')

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
            plugin, module, class_name = load_plugin({'className': site.get('className'), "module": site.get('plugin')})
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
            print(type(inst))
            print(inst.args)
            print(inst)
            pass

    threads = []

    sites = helper.get_sites_config()
    for group in sites:
        if group['version'] > helper.KODI_VERSION or ('searchable' in group and not group['searchable']):
            continue
        for site in group['sites']:
            progress['length'] += 1
            progress['dialog'].create('Processing', "Searching %d/%d sites" % (progress['counter'], progress['length']))
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

        url = plugin.url_for(searching, query=json.dumps({'module': module, 'className': class_name, 'text': text}))
        xbmcplugin.addDirectoryItem(plugin.handle, url, sli, isFolder=True)

        for item in movies['movies'][:5]:
            try:
                list_item = xbmcgui.ListItem(label=item['label'])
                list_item.setLabel2(item['realtitle'])
                list_item.setArt({
                    'thumb': item['thumb'],
                })

                url = plugin.url_for(show_movie, query=json.dumps({
                    'movie_item': item, 'cat_name': 'Search',
                    'module': module, 'className': class_name
                }))
                xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)
            except:
                print(item)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/search')
def search():
    query = json.loads(plugin.args['query'][0])
    instance, module, class_name = load_plugin(query)

    xbmcplugin.setPluginCategory(plugin.handle, 'Search')
    url = plugin.url_for(searching, query=json.dumps({'module': module, 'className': class_name}))

    xbmcplugin.addDirectoryItem(plugin.handle, url,
                                xbmcgui.ListItem(label="[COLOR orange][B]%s[/B][/COLOR]" % "Enter search text ..."),
                                True)

    # Support to save search history
    contents = helper.search_history_get()
    if contents:
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(clear_search),
                                    xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear search text ..."),
                                    True)
        for txt in contents:
            try:
                url = plugin.url_for(searching,
                                     query=json.dumps({'module': module, 'className': class_name, 'text': txt}))
                xbmcplugin.addDirectoryItem(plugin.handle, url,
                                            xbmcgui.ListItem(label="[COLOR blue][B]%s[/B][/COLOR]" % txt), True)
            except:
                pass
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/searching')
def searching():
    query = json.loads(plugin.args['query'][0])
    instance, module, class_name = load_plugin(query)
    text = query.get('text')

    xbmcplugin.setPluginCategory(plugin.handle, 'Search / %s' % text)
    xbmcplugin.setContent(plugin.handle, 'movies')
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
        xbmcplugin.addDirectoryItem(plugin.handle, None, sli, isFolder=False)

        for item in movies['movies']:
            try:
                list_item = xbmcgui.ListItem(label=item['label'])
                list_item.setLabel2(item['realtitle'])
                list_item.setArt({
                    'thumb': item['thumb'],
                })
                url = plugin.url_for(show_movie, query=json.dumps({
                    'movie_item': item, 'cat_name': 'Search',
                    'module': module, 'className': class_name
                }))
                xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)
            except:
                print(item)
    else:
        return

    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/clearSearch')
def clear_search():
    helper.search_history_clear()
    return


@plugin.route('/lastWatched')
def show_last_watched():
    items: dict = helper.get_last_watch_movie()
    if items:
        xbmcplugin.addDirectoryItem(plugin.handle, plugin.url_for(clear_last_watched),
                                    xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear list ..."), True)
        for item in items.values():
            movie = item.get('movie_item')
            list_item = xbmcgui.ListItem(label=movie.get('label'))
            list_item.addContextMenuItems(globalContextMenu())
            list_item.setLabel2(movie.get('realtitle'))
            list_item.setArt({'thumb': movie.get('thumb')})
            if 'poster' in movie:
                list_item.setArt({'poster': movie.get('poster')})
            if 'intro' in movie:
                list_item.setInfo(type='video', infoLabels={'plot': movie.get('intro')})

            url = plugin.url_for(show_movie, query=json.dumps({
                'movie_item': movie, 'cat_name': 'Watching',
                'module': item.get('module'), 'className': item.get('className')
            }))
            xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, isFolder=True)

    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/clearWatched')
def clear_last_watched():
    helper.clear_last_watch_movie()
    return


def load_plugin(args):
    class_name = args.get('className', None)
    module = args.get('module', None)
    print("*********************** Run module: {} - plugin: {}".format(module, class_name))
    return getattr(import_module(module), class_name), module, class_name


def main():
    plugin.run()
