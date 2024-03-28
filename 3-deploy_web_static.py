#!/usr/bin/python3
"""A fabric script that generates a .tgz archive from
the contents of the web_static folder"""
from datetime import datetime
from fabric.api import *
from os import path
import re

env.user = 'ubuntu'
env.hosts = ['34.204.81.235', '18.234.107.45']
env.key_filename = "~/.ssh/id_rsa_alx"


@runs_once
def do_pack():
    """generates a .tgz archive from the
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


def do_deploy(archive_path):
    """Deploys an archive to web servers"""
    # if archive_path is None:
    #     return False
    if not path.exists(archive_path):
        return False

    if put(archive_path, "/tmp/").failed is True:
        return None
    # get the archive filename without extension
    pattern = r'\/([^\/.]+)\.'
    match = re.search(pattern, archive_path)
    pathname = match.group(1)
    # get filename with extension
    fn = archive_path.split('/')[1]
    # create destination folder for unzipping
    destination_path = "/data/web_static/releases/{}".format(pathname)
    cmd = run("mkdir -p {}".format(destination_path))
    if cmd.failed is True:
        return None
    # unzip files to destination folder
    cmd = run("tar -xvzf /tmp/{} -C /data/web_static/releases/{}".format(
         fn, pathname))
    if cmd.failed is True:
        return None
    # delete archive
    cmd = sudo("rm -rf /tmp/{}".format(fn))
    if cmd.failed is True:
        return None
    # delete old symbolic link
    cmd = run("rm -rf /data/web_static/current")
    if cmd.failed is True:
        return None
    # move all contents of decompressed web_static to
    # destination folder, then delete it
    cmd = run("mv /data/web_static/releases/{}/web_static/*\
               /data/web_static/releases/{}".format(pathname, pathname))
    if cmd.failed is True:
        return None
    cmd = run("rm -rf /data/web_static/releases/{}/web_static".format(
        pathname))
    if cmd.failed is True:
        return None
    # add new symbolic link
    cmd = run("ln -sf {} /data/web_static/current".format(destination_path))
    if cmd.failed is True:
        return None
    return True


def deploy():
    """Deploys an archive to web servers"""
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
