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

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # remove file if exist
        run("rm -rf /data/web_static/releases/{}/"
        # create the folder to uncopress the archive to it
        run("sudo mkdir -p /data/web_static/releases/{}/".format(filename))
        # Uncompress the archive
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive, filename))
        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(archive))

        # move the contenet of web_static up
        run("sudo mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/"
            .format(filename, filename))
        # delete web_static dir
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(filename))

        # Delete the symbolic link /data/web_static/current
        run("sudo rm -rf /data/web_static/current")
        # Create a new the symbolic link /data/web_static/current
        # on the web server,
        # linked to the new version of your code
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        return True
    except:
        return False
