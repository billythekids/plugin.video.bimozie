#!/usr/bin/env python
# coding: utf8
import base64
from hashlib import md5
from Cryptodome.Cipher import AES
# from bilutv.cipher import AES


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
