# Setup server using Puppet

exec {'install':
  provider => shell,
  command => '
  sudo apt-get -y update;
  sudo apt-get -y install nginx;
  sudo mkdir -p /data/web_static/releases/test/;
  sudo mkdir -p /data/web_static/shared/;
  echo "Test page" | sudo tee /data/web_static/releases/test/index.html;
  sudo ln -sf /data/web_static/releases/test/ /data/web_static/current;
  sudo chown -R ubuntu:ubuntu /data;
  sudo sed -i "38i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html index.htm;\n}" /etc/nginx/sites-available/default;
  sudo service nginx restart;',
}
