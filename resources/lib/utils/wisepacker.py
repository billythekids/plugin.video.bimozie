# -*- coding: utf-8 -*-
import re


def from_char_code(*args):
    return ''.join(map(chr, args))


class WisePacker:
    @staticmethod
    def decode(text):
        m = re.search("eval\(.*\);}\('(.*)','(.*)','(.*)','(.*)'\)\);", text)
        a = WisePacker.__parse(m.group(1), m.group(2), m.group(3), m.group(4))
        m = re.search("join\(''\);}\('(.*)','(.*)','(.*)','(.*)'\)\);$", a)
        a = WisePacker.__parse(m.group(1), m.group(2), m.group(3), m.group(4))
        m = re.search("join\(''\);}\('(.*)','(.*)','(.*)','(.*)'\)\);$", a)
        a = WisePacker.__parse(m.group(1), m.group(2), m.group(3), m.group(4))
        return a

    @staticmethod
    def __parse(w, i, s, e):
        a = 0
        b = 0
        c = 0
        string1 = []
        string2 = []
        string_len = len(w + i + s + e)

        while True:
            if a < 5:
                string2.append(w[a])
            else:
                if a < len(w):
                    string1.append(w[a])
            a += 1
            if b < 5:
                string2.append(i[b])
            else:
                if b < len(i):
                    string1.append(i[b])
            b += 1
            if c < 5:
                string2.append(s[c])
            else:
                if c < len(s):
                    string1.append(s[c])
            c += 1
            if string_len == len(string1) + len(string2) + len(e):
                break

        raw_string1 = ''.join(string1)
        raw_string2 = ''.join(string2)
        b = 0
        result = []
        for a in range(0, len(string1), 2):
            ll11 = -1
            if ord(raw_string2[b]) % 2: ll11 = 1
            part = raw_string1[a:a + 2]
            result.append(from_char_code(int(part, 36) - ll11))
            b += 1
            if b >= len(string2):
                b = 0

        return ''.join(result)
