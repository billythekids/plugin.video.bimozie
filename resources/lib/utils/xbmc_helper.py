# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import os
import json

addon = xbmcaddon.Addon()
ADDON_ID = addon.getAddonInfo('id')
addon_data_dir = os.path.join(xbmc.translatePath('special://userdata/addon_data').decode('utf-8'), ADDON_ID)


def s2u(s): return s.decode('utf-8') if isinstance(s, str) else s


def getSetting(key):
    return addon.getSetting(key)


def message(message='', title='', timeShown=5000):
    if message:
        title = ': [COLOR blue]%s[/COLOR]' % title if title else ''
        s0 = '[COLOR green][B]Bimozie[/B][/COLOR]' + title
        message = s2u(message)
        s1 = u'[COLOR %s]%s[/COLOR]' % ('red' if '!' in message else 'gold', message)
        message = u'XBMC.Notification(%s,%s,%s)' % (s0, s1, timeShown)
        xbmc.executebuiltin(message.encode("utf-8"))
    else:
        xbmc.executebuiltin("Dialog.Close(all, true)")


def write_file(name, content):
    path = os.path.join(addon_data_dir, name)
    f = open(path, mode='w')
    f.write(content)
    f.close()
    return path


def read_file(name):
    content = None
    try:
        path = os.path.join(addon_data_dir, name)
        f = open(path, mode='r')
        content = f.read()
        f.close()
    except:
        pass
    return content


def search_history_save(search_key):
    if not search_key:
        return

    content = read_file('history.json')
    if content:
        content = json.loads(content)
    else:
        content = []

    idx = next((content.index(i) for i in content if search_key == i), -1)
    if idx >= 0 and len(content) > 0:
        del content[idx]
    elif len(content) >= 20:
        content.pop()

    content.insert(0, search_key)

    path = os.path.join(addon_data_dir, 'history.json')
    with open(path, 'w') as outfile:
        json.dump(content, outfile)


def search_history_clear():
    path = os.path.join(addon_data_dir, 'history.json')
    with open(path, 'w') as outfile:
        json.dump([], outfile)


def search_history_get():
    content = read_file('history.json')
    if content:
        content = json.loads(content)
    else:
        content = []

    return content


def wait(sec):
    xbmc.sleep(sec * 1000)
