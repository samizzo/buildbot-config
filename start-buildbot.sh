#!/bin/bash

export PATH=$PATH:~/.gem/ruby/2.0.0/bin

sleep 20
cd ~/bb
sh buildbot-server.sh stop
sh buildbot-worker.sh stop
sleep 5
sh buildbot-server.sh start
sh buildbot-worker.sh start


