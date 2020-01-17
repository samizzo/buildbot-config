#!/bin/bash

export PATH=/usr/local/bin:$PATH

cd ~

if [ ! -d bb ] ; then mkdir bb ; fi
cd bb

install_master () {
    # Install the buildbot master virtualenv.
    if [ ! -d master ] ; then mkdir master ; fi
    cd master

    virtualenv --no-site-packages --python=/usr/local/bin/python sandbox
    source sandbox/bin/activate

    # Install the buildbot master itself.
    pip install 'buildbot[bundle]' --upgrade

    # Install pyjade because we customise some html templates.
    pip install pyjade

    # GitHubAuth requires this.
    pip install requests

    # Create the master
    buildbot create-master master
}

install_worker() {
    # Install the buildbot worker virtualenv.
    cd ~/bb
    if [ ! -d worker ] ; then mkdir worker ; fi
    cd worker

    virtualenv --no-site-packages --python=/usr/local/bin/python sandbox
    source sandbox/bin/activate

    # Install the buildbot worker itself.
    pip install buildbot-worker --upgrade

    pip install python-dateutil

    # Create the worker.
    buildbot-worker create-worker worker localhost worker pass
}

install_master
install_worker
