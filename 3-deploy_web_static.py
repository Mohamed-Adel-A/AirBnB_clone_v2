#!/usr/bin/python3
"""
a Fabric script
(based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to
your web servers, using the function deploy
"""


from datetime import datetime
from fabric.api import local
from os import path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ['100.25.12.89', '18.206.233.88']


def do_pack():
    """
    Funciton that create tgz archvie from folder
    """
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    tgz_file = "versions/web_static_{}.tgz".format(str(time))

    local("mkdir -p versions")
    r = local("tar -cvzf {} web_static/".format(tgz_file))

    if r.succeeded:
        return (tgz_file)
    else:
        return None


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
    if run("mkdir -p /data/web_static/releases/{}/".format(filename)).failed:
        return False
    # Uncompress the archive
    if (run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive, filename)).failed):
        return False
    # Delete the archive from the web server
    if (run("rm /tmp/{}".format(archive)).failed):
        return False

    # move the contenet of web_static up
    if run("mv /data/web_static/releases/{}/web_static/* \
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
    return True


def deploy():
    """
    Function to deploy web server
    """
    archive = do_back()
    if not archive:
        return (False)
    return do_deploy(archive)
