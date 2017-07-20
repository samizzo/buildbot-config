#!/bin/bash

export PATH=/usr/local/bin:$PATH

cd ~

# Install homebrew.
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update

# Install python2.
# The python that ships with macOS is linked against an outdated OpenSSL and can
# no longer make connections to unity3d.com
brew install python

pip install --upgrade pip

# Install virtualenv.
pip install virtualenv

# Install dateutil
pip install python-dateutil

# Install xcpretty locally and add it to the path.
gem install --user-install xcpretty
