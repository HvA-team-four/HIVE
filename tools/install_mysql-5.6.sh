#!/usr/bin/env bash

apt-get -y remove --purge mysql-server-5.5
apt-get -y autoremove

# Install MySQL Server in a Non-Interactive mode. Default root password will be "root"
echo "mysql-server-5.6 mysql-server/root_password password root" | debconf-set-selections
echo "mysql-server-5.6 mysql-server/root_password_again password root" | debconf-set-selections
apt-get -y install mysql-server-5.6

mysql -u root -proot <<MY_QUERY
CREATE SCHEMA scotchbox;
MY_QUERY

python3.6 /home/vagrant/hive/crawler/utilities/models.py

mysql -u root -proot <<MY_QUERY
USE HIVE;
ALTER TABLE scotchbox.content ADD FULLTEXT (content);
ALTER TABLE scotchbox.content ADD FULLTEXT (content);
MY_QUERY
