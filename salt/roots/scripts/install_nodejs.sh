#!/bin/sh

# Install Node.js
apt-get install python2.7 # Node build script requires Python 2
NODE_VERSION=0.10.23
ARCH=linux-x64
wget -q -c http://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-${ARCH}.tar.gz
tar xz --strip-components=1 -C /usr -f node-v${NODE_VERSION}-${ARCH}.tar.gz
