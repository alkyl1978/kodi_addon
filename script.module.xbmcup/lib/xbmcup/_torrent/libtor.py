# -*- coding: utf-8 -*-

__all__ = ['LibTorrent']


_IS_LIBTORRENT = True

class LibTorrent(object):
    def __init__(self):
        self.support = _IS_LIBTORRENT

    def info(self, torrent):
        pass
