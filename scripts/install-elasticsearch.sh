#!/bin/bash

# install elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.1.deb
sudo dpkg -i elasticsearch-5.1.1.deb

# start elasticsearch on boot
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service

# allow host OS to access through port forwarding
sudo echo "
network.bind_host: 0
network.host: 0.0.0.0" >> /etc/elasticsearch/elasticsearch.yml
sudo sed -i -e '$a\' /etc/elasticsearch/elasticsearch.yml
sudo sed -i -e '$a\' /etc/elasticsearch/elasticsearch.yml

# install Kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-5.1.1-amd64.deb
sha1sum kibana-5.1.1-amd64.deb
sudo dpkg -i kibana-5.1.1-amd64.deb

# allow host OS to access through port forwarding
sudo echo '
server.host: "0.0.0.0"' >> /etc/kibana/kibana.yml
sudo sed -i -e '$a\' /etc/kibana/kibana.yml
sudo sed -i -e '$a\' /etc/kibana/kibana.yml

sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
