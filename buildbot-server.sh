#!/bin/bash

export PATH=/usr/local/bin:$PATH

cd ~/bb/master
source sandbox/bin/activate

if [ "$1" == "stop" ] ; then
    buildbot stop master
else
    buildbot restart master
fi


