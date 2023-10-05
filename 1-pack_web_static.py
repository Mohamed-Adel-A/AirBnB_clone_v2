#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder
of your AirBnB Clone repo, using the function do_pack.
"""

from datetime import datetime
from fabric.api import local


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
