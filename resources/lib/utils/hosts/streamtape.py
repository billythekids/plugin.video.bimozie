# -*- coding: utf-8 -*-
import urlresolver


def get_link(url, media):
    hmf = urlresolver.HostedMediaFile(url=url)
    if not hmf:
        return None, None

    return hmf.resolve(), 'streamtape'
