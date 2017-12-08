#!/usr/bin/env bash

sudo apt-get install libzmq-dev libevent-dev python-dev python-virtualenv -y

virtualenv /opt/circus
cd /opt/circus
bin/pip install circus
