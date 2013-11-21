#!/bin/sh

# Install Python 3
apt-get update
apt-get install libreadline-dev
PYTHON_VERSION=3.3.3
wget -q -c http://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
tar xzf Python-${PYTHON_VERSION}.tgz
cd Python-${PYTHON_VERSION}
sed -ie s/#readline/readline/ Modules/Setup.dist
./configure
make
make install

# Install Node.js
apt-get install python2.7  # Node build script requires Python 2
NODE_VERSION=0.10.22
wget -q -c http://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}.tar.gz
tar xzf node-v${NODE_VERSION}.tar.gz
cd node-v${NODE_VERSION}
PYTHON=/usr/bin/python ./configure
make
make install

# Install LESS
npm -g install less

# Install Yuglify
npm -g install yuglify

# Install packages
apt-get -y install postgresql-9.1 git
