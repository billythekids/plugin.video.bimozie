# -*- coding: utf-8 -*-
import hashlib
import json
import os
import re
import socket
from collections import OrderedDict
from contextlib import closing

from kodi_six import xbmc, xbmcaddon, xbmcvfs, xbmcgui
from kodi_six.utils import py2_decode, py2_encode
from six.moves.urllib.parse import quote, unquote
from six.moves.urllib.parse import urlunsplit, urlsplit

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
KODI_VERSION = int(xbmc.getInfoLabel('System.BuildVersion')[0:2])
addon_data_dir = os.path.join(py2_decode(xbmcvfs.translatePath('special://userdata/addon_data')), ADDON_ID)
REQUEST_CACHE = xbmcvfs.translatePath(os.path.join(addon_data_dir, 'requests_cache'))


def log(msg, level=xbmc.LOGDEBUG):
    xbmc.log("----------------Start Log-----------------", level=level)
    xbmc.log("%s: %s" % ("Bimozie", msg), level=level)
    xbmc.log("---------------- End Log -----------------", level=level)


def s2u(s): return py2_decode(s) if isinstance(s, str) else s


def getSetting(key):
    return ADDON.getSetting(key)


def has_file_path(filename):
    return os.path.exists(get_file_path(filename))


def get_file_path(filename):
    return os.path.join(addon_data_dir, filename)


def get_last_modified_time_file(filename):
    return int(os.path.getmtime(get_file_path(filename)))


def message(message='', title='', time_shown=5000):
    if message:
        title = ': [COLOR blue]%s[/COLOR]' % title if title else ''
        s0 = '[COLOR green][B]Bimozie[/B][/COLOR]' + title
        message = s2u(message)
        s1 = message
        message = 'Notification(%s,%s,%s)' % (s0, s1, time_shown)
        xbmc.executebuiltin(py2_encode(message))
    else:
        xbmc.executebuiltin("Dialog.Close(all, true)")


def write_file(name, content, binary=False):
    if not os.path.exists(addon_data_dir):
        log("********************** create dir path %s" % addon_data_dir)
        os.makedirs(addon_data_dir)

    path = get_file_path(name)
    try:
        write_mode = 'wb+' if binary else 'w+'
        f = open(path, mode=write_mode)
        f.write(content)
        f.close()
    except:
        pass
    return path


def read_file(name, binary=False):
    content = None
    read_mode = 'rb' if binary else 'r'
    try:
        path = get_file_path(name)
        f = open(path, mode=read_mode)
        content = f.read()
        f.close()
    except:
        pass

    return content


def remove_file(filename):
    if has_file_path(filename):
        os.remove(get_file_path(filename))


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


def save_last_watch_movie(query):
    if not query:
        return
    content = read_file('watched.json')
    if content:
        content = json.loads(content, object_pairs_hook=OrderedDict)
    else:
        content = OrderedDict()

    cache_id = hashlib.md5(query.get('movie_item').get('id').encode("utf-8")).hexdigest()
    content.update({cache_id: query})
    content.move_to_end(cache_id, last=False)
    write_file('watched.json', json.dumps(content))


def get_last_watch_movie():
    content = read_file('watched.json')
    if content:
        content = json.loads(content)
    else:
        content = {}
    return content


def clear_last_watch_movie():
    write_file('watched.json', '')


def wait(sec):
    xbmc.sleep(sec * 1000)


def convert_js_2_json(str):
    try:
        return json.loads(str)
    except: pass

    vstr = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)\s?([a-zA-Z][a-zA-Z0-9]*)', r'"\1"', str)
    vstr = re.sub(r'([a-zA-Z][a-zA-Z0-9]*)(?=:)\s?([a-zA-Z][a-zA-Z0-9]*)', r'"\1"', vstr)
    vstr = re.sub(r'\t+\"', '"', vstr)
    vstr = vstr.replace("'", '"')

    return json.loads(vstr)


def fixurl(url):
    # turn string into unicode
    # if not isinstance(url, unicode):
    #     url = url.decode('utf8')

    # parse it
    parsed = urlsplit(url)

    # divide the netloc further
    userpass, at, hostport = parsed.netloc.rpartition('@')
    user, colon1, pass_ = userpass.partition(':')
    host, colon2, port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        quote(unquote(pce).encode('utf8'), '')
        for pce in parsed.path.split('/')
    )
    query = quote(unquote(parsed.query).encode('utf8'), '=&?/')
    fragment = quote(unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user, colon1, pass_, at, host, colon2, port))
    return urlunsplit((scheme, netloc, path, query, fragment))


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


def get_sites_config():
    file_path = os.path.dirname(os.path.abspath(__file__))
    with closing(xbmcvfs.File(file_path + '/../sites.py', 'r')) as json_file:
        sites = json.load(json_file)
    return sites


# Encode text
def text_encode(txt, encoding='utf-8'):
    if 'latin1' in encoding:
        try:
            return txt.encode('latin1').decode('utf-8').strip()
        except:
            return py2_encode(txt, 'latin1').decode('utf-8').strip()

    return py2_encode(txt, encoding)


def save_last_fshare_movie(query):
    if not query:
        return
    content = read_file('fshare-watched.json')
    if content:
        content = json.loads(content, object_pairs_hook=OrderedDict)
    else:
        content = OrderedDict()

    cache_id = hashlib.md5(query.get('link').encode("utf-8")).hexdigest()
    content.update({cache_id: query})
    content.move_to_end(cache_id, last=False)
    write_file('fshare-watched.json', json.dumps(content))


def get_last_fshare_movie():
    content = read_file('fshare-watched.json')
    if content:
        content = json.loads(content)
    else:
        content = {}
    return content


def clear_last_fshare_movie():
    write_file('fshare-watched.json', '')


def extract_domain_port(url):
    base_url = urlparse(url)
    return base_url.netloc, 443 if 'https' in base_url.scheme else 80


def get_host_address_url(url):
    domain, port = extract_domain_port(url)
    address = socket.gethostbyname(domain)
    return url.replace(domain, address)



