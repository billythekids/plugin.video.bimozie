# -*- coding: utf-8 -*-
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer


class Cache:
    def __init__(self, database="whatever"):
        self.cache = StorageServer.StorageServer(database, 24)  # (Your plugin name, Cache time in hours)

    def set(self, key, value):
        self.cache.set(key, value)

    def delete(self, key):
        self.cache.delete(key)

    def get(self, key):
        return self.cache.get(key)

    def setMulti(self, key, array):
        self.cache.setMulti(key, array)

    def getMulti(self, key):
        return self.cache.getMulti(key)
