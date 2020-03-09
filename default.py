# -*- coding: utf-8 -*-

import sys
import os

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, 'resources', 'lib'))
sys.path.append(os.path.join(current_dir, 'resources', 'lib', 'plugins'))

import app

if __name__ == '__main__':
    app.router()
