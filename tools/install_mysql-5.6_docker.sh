#!/usr/bin/env bash

sudo apt-get update
echo "mysql-server-5.6 mysql-server/root_password password root" | debconf-set-selections
echo "mysql-server-5.6 mysql-server/root_password_again password root" | debconf-set-selections
sudo apt-get install mysql-server-5.6 -y
service mysql restart



sudo mysql --host=127.0.0.1 -u root -proot <<MY_QUERY
CREATE SCHEMA hive;
MY_QUERY

python3.6 /opt/crawler/crawler/utilities/models.py

sudo mysql --host=127.0.0.1 -u root -proot <<MY_QUERY
USE hive;
ALTER TABLE hive.content ADD FULLTEXT (content);
ALTER TABLE hive.content ADD FULLTEXT (content);
MY_QUERY

