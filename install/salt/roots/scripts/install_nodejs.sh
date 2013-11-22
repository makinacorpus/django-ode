#!/bin/sh

# Install Node.js
apt-get install python2.7 # Node build script requires Python 2
NODE_VERSION=0.10.22
wget -q -c http://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}.tar.gz
tar xzf node-v${NODE_VERSION}.tar.gz
cd node-v${NODE_VERSION}
PYTHON=/usr/bin/python ./configure
make
make install

