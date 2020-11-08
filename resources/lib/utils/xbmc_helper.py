# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import xbmcgui
import os
import json
import re
import urlparse
import urllib

addon = xbmcaddon.Addon()
ADDON_ID = addon.getAddonInfo('id')
addon_data_dir = os.path.join(xbmc.translatePath('special://userdata/addon_data').decode('utf-8'), ADDON_ID)


def s2u(s): return s.decode('utf-8') if isinstance(s, str) else s


def getSetting(key):
    return addon.getSetting(key)


def has_file_path(filename):
    return os.path.exists(get_file_path(filename))


def get_file_path(filename):
    return os.path.join(addon_data_dir, filename)


def remove_file(filename):
    return os.remove(get_file_path(filename))


def get_last_modified_time_file(filename):
    return int(os.path.getmtime(get_file_path(filename)))


def message(message='', title='', timeShown=5000):
    if message:
        title = ': [COLOR blue]%s[/COLOR]' % title if title else ''
        s0 = '[COLOR green][B]Bimozie[/B][/COLOR]' + title
        message = s2u(message)
        s1 = message
        message = u'XBMC.Notification(%s,%s,%s)' % (s0, s1, timeShown)
        xbmc.executebuiltin(message.encode("utf-8"))
    else:
        xbmc.executebuiltin("Dialog.Close(all, true)")


def write_file(name, content, binary=False):
    if not os.path.exists(addon_data_dir):
        os.makedirs(addon_data_dir)
    path = get_file_path(name)

    try:
        mode = 'w+'
        if binary:
            mode = 'wb+'
        f = open(path, mode=mode)
        f.write(content)
        f.close()
    except:
        pass
    return path


def read_file(name):
    content = None
    try:
        path = get_file_path(name)
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
    write_file('history.json', json.dumps(content))


def search_history_clear():
    write_file('history.json', json.dumps([]))


def search_history_get():
    content = read_file('history.json')
    if content:
        content = json.loads(content)
    else:
        content = []

    return content


def wait(sec):
    xbmc.sleep(sec * 1000)


def convert_js_2_json(str):
    vstr = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', str)
    vstr = vstr.replace("'", '"')
    vstr = re.sub(r'\t+\"', '"', vstr)
    return json.loads(vstr)


def fixurl(url):
    # turn string into unicode
    if not isinstance(url, unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass, at, hostport = parsed.netloc.rpartition('@')
    user, colon1, pass_ = userpass.partition(':')
    host, colon2, port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'), '')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'), '=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user, colon1, pass_, at, host, colon2, port))
    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))


def create_select_dialog(listitems):
    return xbmcgui.Dialog().select("Select item", listitems)


def humanbytes(B):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return '{0:.2f} KB'.format(B / KB)
    elif MB <= B < GB:
        return '{0:.2f} MB'.format(B / MB)
    elif GB <= B < TB:
        return '{0:.2f} GB'.format(B / GB)
    elif TB <= B:
        return '{0:.2f} TB'.format(B / TB)


def sleep(milisecond):
    xbmc.sleep(milisecond)
