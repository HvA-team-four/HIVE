#!/usr/bin/env bash
# taken from https://gist.github.com/cdjhlee/b8e3c927a01b0948b42d

##############################################
#from http://zeromq.org/intro:get-the-software
##############################################

#get zeromq
wget http://download.zeromq.org/zeromq-4.0.5.tar.gz

#unpack tarball package
tar xvzf zeromq-4.0.5.tar.gz

#install dependency
sudo apt-get update && \
sudo apt-get install -y libtool pkg-config build-essential autoconf automake uuid-dev

#in zeromq dir
cd zeromq-4.0.5

#create make file
./configure

#build and install(root permission only)
sudo make install

#install zeromq driver on linux
sudo ldconfig

#check installed
ldconfig -p | grep zmq
############################################################
#libzmq.so.4 (libc6,x86-64) => /usr/local/lib/libzmq.so.4
#libzmq.so (libc6,x86-64) => /usr/local/lib/libzmq.so
############################################################