#!/bin/sh

# Install Python 3
apt-get -y install libreadline-dev
PYTHON_VERSION=3.3.3
wget -q -c http://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
tar xzf Python-${PYTHON_VERSION}.tgz
cd Python-${PYTHON_VERSION}
sed -ie s/#readline/readline/ Modules/Setup.dist
./configure
make
make install
