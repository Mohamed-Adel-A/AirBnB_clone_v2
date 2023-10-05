#!/usr/bin/env bash
# a Bash script that sets up your web servers
# for the deployment of web_static

# install nginx
sudo apt-get update
sudo apt-get install nginx -y

# create folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# create fake html file with content
echo "Test page" > /data/web_static/releases/test/index.html

# create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
chown -R ubuntu:ubuntu /data

# Update the Nginx configuration to serve the content
# of /data/web_static/current/ to hbnb_static
sudo sed -i '38i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n}' /etc/nginx/sites-available/default

# restart nginx
service nginx restart
