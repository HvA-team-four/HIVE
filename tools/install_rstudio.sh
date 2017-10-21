#!/usr/bin/env bash

cd /
sudo apt-get install gdebi-core
sudo wget https://download2.rstudio.org/rstudio-server-1.1.383-amd64.deb
sudo gdebi rstudio-server-1.1.383-amd64.deb
sudo apt-get install python-dev