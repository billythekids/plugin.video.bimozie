import re
from urlparse import urlparse
from utils.mozie_request import Request
from urllib import urlencode
import cors


def get_link(url, media):
    return str(url), 'Google Video'
