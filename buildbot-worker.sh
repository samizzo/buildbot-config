#!/bin/bash

export PATH=/usr/local/bin:$PATH

cd ~/bb/worker
source sandbox/bin/activate

if [ "$1" == "stop" ] ; then
    buildbot-worker stop worker
else
    buildbot-worker start worker
fi


