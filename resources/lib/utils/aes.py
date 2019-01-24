#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from hashlib import md5
from Cryptodome.Cipher import AES
import math
import random


# from bilutv.cipher import AES

def randArr(num):
    return map(lambda i: math.floor(random.random() * 256), xrange(num))


def s2a(s, binary):
    return map(lambda s: ord(s), list(s))


class CryptoAES:
    def unpad(self, data):
        return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

    def bytes_to_key(self, data, salt, output=48):
        # extended from https://gist.github.com/gsakkis/4546068
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]

    def decrypt(self, encrypted, passphrase):
        encrypted = base64.b64decode(encrypted)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        key_iv = self.bytes_to_key(passphrase, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return self.unpad(aes.decrypt(encrypted[16:])).decode('utf-8')
        # return self.unpad(AES(key).decrypt_cbc(encrypted[16:], iv)).decode('utf-8')

# key = "bilutv.net45904818777474"
# text = "U2FsdGVkX1/xkligkvgVuR+lAuySrbwvVQPSbL4PkvxOZ+wqb/TvwWpc5/SLcwdiZAZxQeyAo//en5ROfpMFmKX0+qOAQiPHmG3q2sFIHhvD1et534gsrcnkVuXqJg8Gxr8jy4nJRkyFi0mBa2gZbMCrTOsgVqE4jD+gyyWdGLUGaoEoNuGUU053gIMWtzkLeNSDhnH6e6NZYQax5ctawMPM0IB2FxPrQ+fMW6Pey4FHJgfakXTwcPJM/7ZbArJoaLnjH/F+Pp3mTrgSk2AYb6CgMGWI8kXGuCC1edvbSwrAkRFLNCoafanpcM3MIoGZ"

# value = CryptoAES().decrypt(text, bytes(key.encode('utf-8')))
# print(value)

# key="2HybsHfda81sj01545544327e4f60ae9"
# text="U2FsdGVkX186iQkL7vT5fjVazd+/+r0eakDVmPrmUrNkmnb8BPps4Nbtq9r/+Pl6P7JrmmlTsTNbqC2nI0VtcT2OiDbhXCVRv6q/w4Eegr7jJf8VaJmbYCrJ7RN+W0odsHlrLEiFjrsPwgoWGKIx64vT8wiS8d1s0bf+uvH1y/Ad5mV0ettppiEeZD1OFWo6qqApl9lAi0sb9cdiQhQAlVTPYHAyEhM9NwqUd6YyL8+euOjgh+aML5xd1GPZJ7oRYd7anjEC/KuQXSsVB/BAL50+98gbx8H14zlVKGLVNCCcIffK69JLX4jImq/SgcruF8wA+T2qytGMOrzccQi9a9rzKG2g3snuz93QuN+RN03KMZhyVz+eEIMqeEivLZUH/fbgzPZ1Q0nnhOibt77dtdnPRia31GpmzPNeqHdp5bFEdyHcu6IztmiRYGzIxHGA/rRWniP5ldHu0FZSNo3PuNeFVhg3D4VikMhUfdAYK3JHEjsBgxxdd2Qu2GwS3qA7LZeFe5UdkGmJO9pt0nUQ87e2VzjPOitziDlSZXLw0G47UnPWgPnz/tEJ0AYaBRszNAnLMPuhr4x25UvD/zwE8jjhPlDL/ouYgZexxAYoIh+Y6mhgO3hNwe7mFocOeaDN7vE0jsCXLyj1P2DHGyaroIKCAXcsjoE4fkzLE48OLITyz3gtDlMyK32azKHiXNijs5dMalMTz5lC/WC4ojt9PE0PzC9BCcyE1Z9o6BsDZP4vcrLP5bS/4zVE5dIEb6gsCp982Dy+KxD8n0RqyE86FKM6x5i9t6ajId6KlpDioL+0BfkXnY88vyVWPULcVELBFujNODBgTVWpSgHKtXjVrSgUU40FEybc9ZLAbOgH/dY="
#
# value = CryptoAES().decrypt(text, bytes(key.encode('utf-8')))
# print(value)