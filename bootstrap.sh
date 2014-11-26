#!/usr/bin/env bash

echo "Install and dependencies"
#sudo apt-get update
#sudo apt-get install -y python-dev libpq-dev build-essential libssl-dev libffi-dev

echo "Install Nginx"
#sudo apt-get install -y nginx

echo "Install postgresql"
#sudo apt-get install -y postgresql python-psycopg2

echo "Install mercurial and git"
#sudo apt-get install -y mercurial git

echo "Install pip"
#sudo apt-get install -y python-pip

echo "Install virtual environment"
#sudo pip install virtualenv
cd /vagrant
#virtualenv venv

echo "Enable virtual environment and dependencies"
source venv/bin/activate
pip install -r requirements.txt
