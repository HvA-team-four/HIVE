#!/usr/bin/env bash

sudo echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list
sudo echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list

sudo gpg --keyserver keys.gnupg.net --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89
sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -

sudo apt-get update -y

sudo apt-get install tor deb.torproject.org-keyring -y





