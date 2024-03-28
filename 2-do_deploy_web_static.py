#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from
the contents of the web_static folder and deploys it to
a web server"""

from fabric.api import *
from os import path
import re

env.user = 'ubuntu'
env.hosts = ['34.204.81.235', '18.234.107.45']
env.key_filename = "~/.ssh/id_rsa_alx"


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
