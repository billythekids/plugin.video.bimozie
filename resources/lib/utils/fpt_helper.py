# -*- coding: utf-8 -*-

import time
import hashlib
import xbmc_helper as helper

api_token = "WEBv6Dkdsad90dasdjlALDDDS"
suffix = "/api/v6.1_w/"
domain = "https://api.fptplay.net"


def generate_stoken(path):
    a = int(time.time()) + 10800
    o = path

    token = "%s%s%s%s" % (api_token, a, suffix, o)

    m = hashlib.md5()
    m.update(token)
    return unknown_encrypt(m.hexdigest()), a


def unknown_encrypt(e):
    n = []
    t = e.upper()
    r = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    for o in range(int(len(t) / 2)):
        i = t[2 * o:2 * o + 2]
        num = '0x%s' % i
        n.append(int(num, 16))

    def convert(e):
        t = ""
        n = 0
        o = 0
        i = [0, 0, 0]
        a = [0, 0, 0, 0]
        s = len(e)
        c = 0

        for z in range(s, 0, -1):
            if n <= 3:
                i[n] = e[c]

            n += 1
            c += 1
            if 3 == n:
                a[0] = (252 & i[0]) >> 2
                a[1] = ((3 & i[0]) << 4) + ((240 & i[1]) >> 4)
                a[2] = ((15 & i[1]) << 2) + ((192 & i[2]) >> 6)
                a[3] = (63 & i[2])
                for v in range(4):
                    t += r[a[v]]
                n = 0

        if n:
            for o in range(n, 3, 1):
                i[o] = 0

            for o in range(n+1):
                a[0] = (252 & i[0]) >> 2
                a[1] = ((3 & i[0]) << 4) + ((240 & i[1]) >> 4)
                a[2] = ((15 & i[1]) << 2) + ((192 & i[2]) >> 6)
                a[3] = (63 & i[2])
                t += r[a[o]]
            n += 1
            while n < 3:
                t += "="
                n += 1

        return t

    return convert(n).replace('+', '-').replace('/', '_').replace('=', '')