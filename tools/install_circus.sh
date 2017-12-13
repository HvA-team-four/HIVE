#!/usr/bin/env bash

sudo apt-get install libzmq-dev libevent-dev python-dev python-virtualenv -y

virtualenv /opt/HIVE
cd /opt/HIVE
bin/pip install circus
