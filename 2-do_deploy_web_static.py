#!/usr/bin/python3
"""
a Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy
"""

from os import path
from fabric.api import local
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ['100.25.12.89', '18.206.233.88']


def do_deploy(archive_path):
    """
    Function to deploy archive to the servers
    """
    if not path.exists(archive_path):
        return (False)

    archive = archive_path.split('/')[-1]
    filename = archive.split('.')[0]

    # Upload the archive to the /tmp/ directory of the web server
    if put(archive_path, "/tmp/").failed:
        return False
    # create the folder to uncopress the archive to it
    if run("sudo mkdir -p /data/web_static/releases/{}/".format(filename)).failed:
        return False
    # Uncompress the archive
    if (run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive, filename)).failed):
        return False
    # Delete the archive from the web server
    if (run("sudo rm /tmp/{}".format(archive)).failed):
        return False

    # move the contenet of web_static up
    if run("sudo mv /data/web_static/releases/{}/web_static/* \
    /data/web_static/releases/{}/"
           .format(filename, filename)).failed:
        return False
    # delete web_static dir
    if run("sudo rm -rf /data/web_static/releases/{}/web_static"
           .format(filename)).failed:
        return False

    # Delete the symbolic link /data/web_static/current
    if run("sudo rm -rf /data/web_static/current").failed:
        return False
    # Create a new the symbolic link /data/web_static/current
    # on the web server,
    # linked to the new version of your code
    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
           .format(filename)).failed:
        return False
    print("New version deployed!")
    return True
