# -*- coding: utf-8 -*-
import sys
import re
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import json
from importlib import import_module
from utils.media_helper import MediaHelper
from threading import Thread
import utils.xbmc_helper as XbmcHelper

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASEURL = sys.argv[0]
ARGS = urlparse.parse_qs(sys.argv[2][1:])
ADDON_ID = ADDON.getAddonInfo('id')
KODI_VERSION = int(xbmc.getInfoLabel('System.BuildVersion')[0:2])

print("***********************Current version %d" % KODI_VERSION)

SITES = [
    {
        'name': 'fptplay.vn',
        'logo': 'https://fptplay.vn/images/logo.png',
        'className': 'Fptplay',
        'plugin': 'fptplay.plugin',
        'version': 1
    },
    {
        'name': 'vkool.tv',
        'logo': 'https://i.ibb.co/TcWtgB5/rsz-image.png',
        'className': 'Vkool',
        'plugin': 'vkool.plugin',
        'version': 1
    },
    {
        'name': 'fimfast.com',
        'logo': 'https://fimfast.com/assets/img/logo.png',
        'className': 'Fimfast',
        'plugin': 'fimfast.plugin',
        'version': 1
    },

    {
        'name': 'bilutv.org',
        'logo': 'http://bilutv.org/Theme/images/bilutv-logo-noel.png',
        'className': 'Bilutv',
        'plugin': 'bilutv.plugin',
        'version': 1
    },
    {
        'name': 'phimmedia.tv',
        'logo': 'http://www.phimmedia.tv/templates/themes/phim/images/phimmedia-s.png',
        'className': 'Phimmedia',
        'plugin': 'phimmedia.plugin',
        'version': 1
    },
    {
        'name': 'phimmoi.net',
        'logo': 'http://www.phimmoi.net/logo/phimmoi-square.png',
        'className': 'Phimmoi',
        'plugin': 'phimmoi.plugin',
        'version': 18
    },
    {
        'name': 'hphim.net',
        'logo': 'https://i.ibb.co/fH1RNxH/image.png',
        'className': 'Hphim',
        'plugin': 'hphim.plugin',
        'version': 1
    },
    {
        'name': 'tvhay.org',
        'logo': 'https://kodi-addons.club/data/d1/d14a048c56373761664ca89a773d694d.png',
        'className': 'Tvhay',
        'plugin': 'tvhay.plugin',
        'version': 1
    },
    {
        'name': 'phim3s.pw',
        'logo': 'http://cdn.marketplaceimages.windowsphone.com/v8/images/3143b748-2dd8-4b88-874c-72c0e9542cd1?imageType=ws_icon_medium',
        'className': 'Phim3s',
        'plugin': 'phim3s.plugin',
        'version': 31
    },
    {
        'name': 'phimbathu.org',
        'logo': 'http://phimbathu.org/Theme/images/phimbathu-logo.png',
        'className': 'Phimbathu',
        'plugin': 'phimbathu.plugin',
        'version': 1
    },
    {
        'name': 'kenh88.com',
        'logo': 'http://www.kenh88.com/images/logo_kenh88.png',
        'className': 'Kenh88',
        'plugin': 'kenh88.plugin',
        'version': 1
    },
    {
        'name': 'phim14.net',
        'logo': 'http://phim14.net/application/views/frontend/default/images/logo.png',
        'className': 'Phim14',
        'plugin': 'phim14.plugin',
        'version': 1
    },
    {
        'name': 'fcine.net',
        'logo': 'https://fcine.net/uploads/monthly_2019_01/FCINE-LOGO.png.0d4b6b0253c4fd8a4dbefa7067ac0ac4.png',
        'className': 'Fcine',
        'plugin': 'fcine.plugin',
        'version': 31
    },
    {
        'name': 'animehay.tv',
        'logo': 'https://i1.wp.com/www.albertgyorfi.com/wp-content/uploads/2017/05/anime-pack.png?fit=256%2C256&ssl=1',
        'className': 'Animehay',
        'plugin': 'animehay.plugin',
        'version': 1
    },
    {
        'name': 'vuviphim.com',
        'logo': 'https://vuviphim.com/wp-content/uploads/2017/08/logo-vuviphim.png',
        'className': 'Vuviphim',
        'plugin': 'vuviphim.plugin',
        'version': 1
    },
    {
        'name': 'vtv16.com',
        'logo': 'https://yt3.ggpht.com/a-/AN66SAx84wKI577rKgX2IeQUiG31GaOhmVIu2le2rQ=s900-mo-c-c0xffffffff-rj-k-no',
        'className': 'Vtv16',
        'plugin': 'vtv16.plugin',
        'version': 1
    },
    {
        'name': 'phimgi.net',
        'logo': 'https://cdn-img.phimgi.net/wp-content/uploads/2019/01/phimgi-02.png',
        'className': 'Phimgi',
        'plugin': 'phimgi.plugin',
        'version': 1
    },
    {
        'name': 'dongphim.net',
        'logo': 'http://media.dongphim.net/media/image/id/5c921766acc399d72c8b456b_200x',
        'className': 'Dongphim',
        'plugin': 'dongphim.plugin',
        'version': 1
    },
    {
        'name': 'hdvietnam.com (beta)',
        'logo': 'http://www.hdvietnam.com/images/hd-vietnam-logo.png',
        'className': 'Hdvietnam',
        'plugin': 'hdvietnam.plugin',
        'version': 1
    },
    {
        'name': 'xemphim.plus',
        'logo': 'https://xemphim.plus/static/skin/logo-full.png',
        'className': 'Xemphim',
        'plugin': 'xemphim.plugin',
        'version': 1
    },
]


def build_url(query):
    """build the plugin url"""
    return BASEURL + '?' + urllib.urlencode(query)


def globalContextMenu():
    commands = list()
    commands.append(('Settings', 'Addon.OpenSettings(%s)' % ADDON_ID,))
    return commands


def onInit():
    xbmcplugin.setPluginCategory(HANDLE, 'Websites')
    xbmcplugin.setContent(HANDLE, 'movies')

    # show global search link
    url = build_url({'mode': 'globalsearch'})
    xbmcplugin.addDirectoryItem(HANDLE, url,
                                xbmcgui.ListItem(label="[COLOR yellow][B] %s [/B][/COLOR]" % "Search All..."), True)

    for site in SITES:
        if site['version'] > KODI_VERSION:
            print("***********************Skip version %d" % site['version'])
            continue

        list_item = xbmcgui.ListItem(label=site['name'])
        list_item.addContextMenuItems(globalContextMenu())
        list_item.setArt({'thumb': site['logo'], 'icon': site['logo']})
        url = build_url({'mode': 'category', 'module': site['plugin'], 'className': site['className']})
        is_folder = True
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)


def list_category(cats, module, classname, movies=None):
    xbmcplugin.setPluginCategory(HANDLE, classname)
    xbmcplugin.setContent(HANDLE, 'files')

    # show search link
    url = build_url({'mode': 'search', 'module': module, 'className': classname})
    xbmcplugin.addDirectoryItem(HANDLE, url,
                                xbmcgui.ListItem(label="[COLOR green][B] %s [/B][/COLOR]" % "Search ..."), True)

    for cat in cats:
        list_item = xbmcgui.ListItem(label=cat['title'])
        list_item.addContextMenuItems(globalContextMenu())
        if 'subcategory' in cat and cat['subcategory'] and len(cat['subcategory']) > 0:
            url = build_url({'mode': 'category', 'url': cat['link'], 'name': cat['title'],
                             'subcategory': json.dumps(cat['subcategory']), 'module': module, 'className': classname})
        else:
            url = build_url({'mode': 'movies', 'url': cat['link'], 'page': 1, 'module': module, 'className': classname})
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, isFolder=True)

    if movies and len(movies) > 0:
        label = "[COLOR yellow][B][---- New Movies ----][/B][/COLOR]"
        sli = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(HANDLE, None, sli, isFolder=False)
        list_movie(movies, '/', 1, module, classname)
    else:
        xbmcplugin.endOfDirectory(HANDLE)


def list_movie(movies, link, page, module, classname):
    xbmcplugin.setPluginCategory(HANDLE, classname)
    xbmcplugin.setContent(HANDLE, 'movies')

    if movies is not None:
        for item in movies['movies']:
            try:
                list_item = xbmcgui.ListItem(label=item['label'])
                list_item.addContextMenuItems(globalContextMenu())
                list_item.setLabel2(item['realtitle'])
                list_item.setIconImage('DefaultVideo.png')
                list_item.setArt({'thumb': item['thumb']})
                if 'poster' in item:
                    list_item.setArt({'poster': item['poster']})
                if 'intro' in item:
                    list_item.setInfo(type='video', infoLabels={'plot': item['intro']})
                url = build_url(
                    {'mode': 'movie', 'url': item['id'], 'thumb': item['thumb'], 'title': item['realtitle'] and item['realtitle'] or item['title'],
                     'module': module, 'className': classname})
                is_folder = True
                xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
            except:
                print(item)

        print("***********************Current page %d" % page)
        # show next page
        if movies['page'] > 1 and page < movies['page']:
            label = "Next page %d / %d >>" % (page, movies['page'])
            next_item = xbmcgui.ListItem(label=label)
            if 'page_patten' in movies and movies['page_patten'] is not None:
                link = movies['page_patten']

            url = build_url({'mode': 'movies', 'url': link, 'page': page + 1, 'module': module, 'className': classname})
            xbmcplugin.addDirectoryItem(HANDLE, url, next_item, True)
    else:
        return
    xbmcplugin.endOfDirectory(HANDLE)


def show_episode(movie, thumb, title, module, class_name):
    if len(movie['episode']) > 0:  # should not in use anymore
        for item in movie['episode']:
            li = xbmcgui.ListItem(label=item['title'])
            li.setInfo('video', {'title': item['title']})
            li.setProperty('fanart_image', thumb)
            li.setArt({'thumb': thumb})
            url = build_url({'mode': 'play',
                             'title': title,
                             'thumb': thumb,
                             'url': json.dumps(item),
                             'direct': 0,
                             'module': module,
                             'className': class_name})
            li.setProperty("IsPlayable", "true")
            xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=True)

    elif len(movie['group']) > 0:
        idx = 0
        for key, items in movie['group'].iteritems():
            idx += 1
            label = "[COLOR red][B][---- %s : [COLOR yellow]%d eps[/COLOR] ----][/B][/COLOR]" % (key, len(items))
            sli = xbmcgui.ListItem(label=label)
            if len(items) < 5 or len(movie['group']) < 1:
                xbmcplugin.addDirectoryItem(HANDLE, None, sli, isFolder=False)
                _build_ep_list(items, title, thumb, module, class_name)
            elif idx is len(movie['group']):
                xbmcplugin.addDirectoryItem(HANDLE, None, sli, isFolder=False)
                _build_ep_list(items, title, thumb, module, class_name)
            else:
                url = build_url({'mode': 'server',
                                 'title': title,
                                 'server': key,
                                 'thumb': thumb,
                                 'items': json.dumps(items),
                                 'module': module,
                                 'className': class_name})
                xbmcplugin.addDirectoryItem(HANDLE, url, sli, isFolder=True)
    else:
        return

    xbmcplugin.setPluginCategory(HANDLE, title)
    xbmcplugin.setContent(HANDLE, 'movies')
    xbmcplugin.endOfDirectory(HANDLE)


def _build_ep_list(items, title, thumb, module, class_name):
    for item in items:
        li = xbmcgui.ListItem(label=item['title'])
        li.setInfo('video', {'title': item['title']})
        li.setProperty('fanart_image', thumb)
        li.setArt({'thumb': thumb})
        movie_title = title
        # try:
        #     movie_title = "[%s] %s" % (item['title'], title)
        # except:
        #     pass

        url = build_url({'mode': 'play',
                         'title': movie_title,
                         'thumb': thumb,
                         'url': json.dumps(item),
                         'direct': 0,
                         'module': module,
                         'className': class_name})
        li.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(HANDLE, url, li, isFolder=False)


def show_server_links(items, title, thumb, server, module, class_name):
    xbmcplugin.setPluginCategory(HANDLE, "%s - %s " % (title, server))
    xbmcplugin.setContent(HANDLE, 'videos')

    label = "[COLOR red][B][---- %s : [COLOR yellow]%d eps[/COLOR] ----][/B][/COLOR]" % (server, len(items))
    sli = xbmcgui.ListItem(label=label)
    xbmcplugin.addDirectoryItem(HANDLE, None, sli, isFolder=False)
    _build_ep_list(items, title, thumb, module, class_name)
    xbmcplugin.endOfDirectory(HANDLE)


def show_links(movie, title, thumb, module, class_name):
    if len(movie['links']) == 0:
        return

    print("***********************Found Total Link %d" % len(movie['links']))
    xbmcplugin.setPluginCategory(HANDLE, title)
    xbmcplugin.setContent(HANDLE, 'movies')
    for item in movie['links']:
        li = xbmcgui.ListItem(label=item['title'])
        li.setInfo('video', {'title': item['title']})
        li.setProperty('fanart_image', thumb)
        li.setArt({'thumb': thumb})

        url = build_url({'mode': 'play',
                         'title': title,
                         'thumb': thumb,
                         'url': json.dumps(item),
                         'direct': 1,
                         'module': module,
                         'className': class_name})
        li.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(HANDLE, url, li, False)

    xbmcplugin.endOfDirectory(HANDLE)


def play(movie, title=None, thumb=None, direct=False):
    print("*********************** playing %s" % title)

    if direct:
        mediatype = MediaHelper.resolve_link(movie)
        play_item = xbmcgui.ListItem()
        play_item.setPath(movie['link'])
    else:
        if not movie or 'links' not in movie or len(movie['links']) == 0:
            return
        else:
            if len(movie['links']) > 1:
                # sort all links
                try:
                    movie['links'] = sorted(movie['links'],
                                            key=lambda elem: re.search(r'(\d+)', elem['title'])
                                                             and int(re.search(r'(\d+)', elem['title']).group(1))
                                                             or 0, reverse=True)
                except Exception as e:
                    print(e)

                # blacklist link
                blacklist = ['hydra', 'maya.bbigbunny.ml', 'smamuhh1metro']

                def filter_blacklist(m):
                    for i in blacklist:
                        if i in m['link']: return False
                    return True

                movie['links'] = list(filter(filter_blacklist, movie['links']))
                listitems = ["%s (%s)" % (i["title"], i["link"]) for i in movie['links']]
                index = xbmcgui.Dialog().select("Select stream", listitems)
                if index == -1:
                    return None
                else:
                    movie = movie['links'][index]
            else:
                movie = movie['links'][0]

            mediatype = MediaHelper.resolve_link(movie)
            play_item = xbmcgui.ListItem()
            play_item.setPath(movie['link'])

    if not movie['link']: return

    if 'subtitle' in movie and movie['subtitle']:
        if isinstance(movie['subtitle'], list):
            play_item.setSubtitles(movie['subtitle'])
        else:
            play_item.setSubtitles([movie['subtitle']])

    if mediatype == 'hls':
        play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        link = movie['link'].split('|')
        if link and len(link) > 1:
            play_item.setProperty('inputstream.adaptive.stream_headers', link[1])

        play_item.setContentLookup(False)

    play_item.setProperty('IsPlayable', 'true')
    # update title
    try:
        play_item.setInfo('video', {'title': "[%s] %s" % (movie['title'], title)})
        play_item.setInfo('video', {'originaltitle': title})
        play_item.setInfo('video', {'sorttitle': title})
    except:
        print(movie['title'], title)

    play_item.setArt({'thumb': thumb})

    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)


def dosearch(plugin, module, classname, text, page=1, recall=False):
    xbmcplugin.setPluginCategory(HANDLE, 'Search Result')
    xbmcplugin.setContent(HANDLE, 'movies')
    if not text:
        keyboard = xbmc.Keyboard('', 'Search iPlayer')
        keyboard.doModal()
        if keyboard.isConfirmed():
            text = keyboard.getText()

    if not text:
        return

    XbmcHelper.search_history_save(text)
    print("*********************** searching %s" % text)
    movies = plugin().search(text)

    if movies is not None:
        label = "[COLOR red][B][---- %s : [COLOR yellow]%d found[/COLOR] View All ----][/B][/COLOR]" % (
            classname, len(movies['movies']))
        sli = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(HANDLE, None, sli, isFolder=False)

        for item in movies['movies']:
            try:
                list_item = xbmcgui.ListItem(label=item['label'])
                list_item.setLabel2(item['realtitle'])
                list_item.setIconImage('DefaultVideo.png')
                list_item.setArt({
                    'thumb': item['thumb'],
                })
                url = build_url(
                    {'mode': 'movie', 'url': item['id'], 'thumb': item['thumb'], 'title': item['title'],
                     'module': module, 'className': classname})
                is_folder = True
                xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
            except:
                print(item)
    else:
        return

    if not recall:
        xbmcplugin.endOfDirectory(HANDLE)


def search(module, classname=None):
    xbmcplugin.setPluginCategory(HANDLE, 'Search')
    xbmcplugin.setContent(HANDLE, 'movies')
    url = build_url({'mode': 'dosearch', 'module': module, 'className': classname})
    xbmcplugin.addDirectoryItem(HANDLE,
                                url,
                                xbmcgui.ListItem(label="[COLOR orange][B]%s[/B][/COLOR]" % "Enter search text ..."),
                                True)

    # Support to save search history
    contents = XbmcHelper.search_history_get()
    if contents:
        url = build_url({'mode': 'clearsearch', 'module': module, 'className': classname})
        xbmcplugin.addDirectoryItem(HANDLE,
                                    url,
                                    xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear search text ..."),
                                    True)
        for txt in contents:
            try:
                url = build_url({'mode': 'dosearch', 'module': module, 'className': classname, 'url': txt})
                xbmcplugin.addDirectoryItem(HANDLE,
                                            url,
                                            xbmcgui.ListItem(label="[COLOR blue][B]%s[/B][/COLOR]" % txt),
                                            True)
            except:
                pass
    xbmcplugin.endOfDirectory(HANDLE)


def global_search():
    xbmcplugin.setPluginCategory(HANDLE, 'Search')
    xbmcplugin.setContent(HANDLE, 'movies')
    url = build_url({'mode': 'doglobalsearch'})
    xbmcplugin.addDirectoryItem(HANDLE,
                                url,
                                xbmcgui.ListItem(label="[COLOR orange][B]%s[/B][/COLOR]" % "Enter search text ..."),
                                True)

    # Support to save search history
    contents = XbmcHelper.search_history_get()
    if contents:
        url = build_url({'mode': 'clearsearch'})
        xbmcplugin.addDirectoryItem(HANDLE,
                                    url,
                                    xbmcgui.ListItem(label="[COLOR red][B]%s[/B][/COLOR]" % "Clear search text ..."),
                                    False)
        for txt in contents:
            try:
                url = build_url({'mode': 'doglobalsearch', 'url': txt})
                xbmcplugin.addDirectoryItem(HANDLE,
                                            url,
                                            xbmcgui.ListItem(label="[COLOR blue][B]%s[/B][/COLOR]" % txt),
                                            True)
            except:
                pass
    xbmcplugin.endOfDirectory(HANDLE)


def do_global_search(text):
    xbmcplugin.setPluginCategory(HANDLE, 'Search Result')
    xbmcplugin.setContent(HANDLE, 'movies')
    if not text:
        keyboard = xbmc.Keyboard('', 'Search iPlayer')
        keyboard.doModal()
        if keyboard.isConfirmed():
            text = keyboard.getText()

    if not text:
        return

    XbmcHelper.search_history_save(text)

    print("*********************** searching %s" % text)

    def _search(plugin, module, classname, text):
        movies = None
        try:
            movies = plugin().search(text)
        except:
            pass
        if movies is not None:
            label = "[COLOR red][B][---- %s : [COLOR yellow]%d found[/COLOR] View All ----][/B][/COLOR]" % (
                classname, len(movies['movies']))
            sli = xbmcgui.ListItem(label=label)
            url = build_url({'mode': 'dosearch', 'module': module, 'className': classname, 'url': text})
            xbmcplugin.addDirectoryItem(HANDLE, url, sli, isFolder=True)
            for item in movies['movies'][:5]:
                try:
                    list_item = xbmcgui.ListItem(label=item['label'])
                    list_item.setLabel2(item['realtitle'])
                    list_item.setIconImage('DefaultVideo.png')
                    list_item.setArt({
                        'thumb': item['thumb'],
                    })
                    url = build_url(
                        {'mode': 'movie', 'url': item['id'], 'thumb': item['thumb'], 'title': item['title'],
                         'module': module, 'className': classname})
                    is_folder = True
                    xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
                except:
                    print(item)

    threads = []
    for site in SITES:
        if site['version'] > KODI_VERSION:
            continue

        plugin, module, classname = get_plugin({'className': [site['className']], "module": [site['plugin']]})
        process = Thread(target=_search, args=[plugin, module, classname, text])
        process.setDaemon(True)
        process.start()
        threads.append(process)

    for process in threads:
        process.join()
    xbmcplugin.endOfDirectory(HANDLE)


def get_plugin(args):
    classname = args.get('className', None)[0]
    module = args.get('module', None)[0]
    print("*********************** Run module: %s - plugin: %s " % (module, classname))
    return getattr(import_module(module), classname), module, classname


def router():
    mode = ARGS.get('mode', None)
    instance = module = classname = None

    if mode is not None and mode[0] != 'globalsearch' and mode[0] != 'doglobalsearch' and mode[0] != 'clearsearch':
        instance, module, classname = get_plugin(ARGS)

    if mode is None:
        onInit()

    elif mode[0] == 'category':
        if 'subcategory' in ARGS:
            list_category(cats=json.loads(ARGS.get('subcategory')[0]), module=module, classname=classname)
        else:
            cats, movies = instance().getCategory()
            list_category(cats=cats, movies=movies, module=module, classname=classname)

    elif mode[0] == 'movies':
        link = ARGS.get('url')[0]
        page = int(ARGS.get('page')[0])
        print("*********************** Display %s page %s" % (link, page))
        movies = instance().getChannel(link, page)
        list_movie(movies, link, page, module, classname)

    elif mode[0] == 'movie':
        id = ARGS.get('url')[0]
        thumb = ARGS.get('thumb')[0]
        title = ARGS.get('title')[0]
        movie = instance().getMovie(id)
        print("*********************** Display movie %s %s" % (title, id))
        if len(movie['episode']) > 0 or len(movie['group']) > 0:
            show_episode(movie, thumb, title, module, classname)
        else:
            show_links(movie, title, thumb, module, classname)

    elif mode[0] == 'server':
        thumb = ARGS.get('thumb')[0]
        title = ARGS.get('title')[0]
        server = ARGS.get('server')[0]
        items = json.loads(ARGS.get('items')[0])
        show_server_links(items, title, thumb, server, module, classname)

    elif mode[0] == 'links':
        url = ARGS.get('url')[0]
        title = ARGS.get('title')[0]
        thumb = ARGS.get('thumb')[0]
        print("*********************** Get Movie Link %s" % url)
        movie = instance().getLink(url)
        show_links(movie, title, thumb, module, classname)

    elif mode[0] == 'play':
        print("*********************** Play movie")
        url = ARGS.get('url')[0]
        title = ARGS.get('title')[0]
        thumb = ARGS.get('thumb')[0]
        direct = int(ARGS.get('direct')[0])
        if direct is 0:
            movie = instance().getLink(json.loads(url))
        else:
            movie = json.loads(url)
        play(movie, title, thumb, direct)

    elif mode[0] == 'search':
        search(module, classname)

    elif mode[0] == 'globalsearch':
        global_search()
    elif mode[0] == 'doglobalsearch':
        text = ARGS.get('url') and ARGS.get('url')[0] or None
        do_global_search(text)

    elif mode[0] == 'dosearch':
        text = ARGS.get('url') and ARGS.get('url')[0] or None
        dosearch(instance, module, classname, text)

    elif mode[0] == 'clearsearch':
        XbmcHelper.search_history_clear()
        return
