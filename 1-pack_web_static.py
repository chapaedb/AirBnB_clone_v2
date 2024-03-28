#!/usr/bin/python3
"""fabric script that generates a .tgz archive from
the contents of the web_static folder"""
from datetime import datetime
from fabric.api import *


def do_pack():
    """ this one generates a .tgz archive from the
    contents of the web_static folder"""
    tp = datetime.now()
    filename = "web_static_{}.tgz".format(tp.strftime("%Y%m%d%H%M%S"))
    res = local('mkdir -p versions', capture=True)
    if res.return_code != 0:
        return None
    res = local("tar -czf versions/{} ./web_static".format(filename),
                capture=True)
    if res.return_code != 0:
        return None
    return "versions/{}".format(filename)
