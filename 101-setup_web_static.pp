# Setup server using Puppet

exec { 'setting up server':
  command => 'sudo apt-get update;
  sudo apt-get install nginx -y;
  mkdir -p /data/web_static/releases/test/;
  mkdir -p /data/web_static/shared/;
  echo "Test page" > /data/web_static/releases/test/index.html;
  ln -sf /data/web_static/releases/test/ /data/web_static/current;
  chown -R ubuntu:ubuntu /data;
  sudo sed -i "38i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n}" /etc/nginx/sites-available/default;
  sudo service nginx restart;'
  provider => shell,
}
