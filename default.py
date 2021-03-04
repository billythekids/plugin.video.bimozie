# -*- coding: utf-8 -*-

import sys
import os

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, 'resources', 'lib'))
sys.path.append(os.path.join(current_dir, 'resources', 'lib', 'plugins'))
sys.path.append(os.path.join(current_dir, 'resources', 'lib', 'utils'))

from resources.lib import app

if __name__ == '__main__':
    app.main()
