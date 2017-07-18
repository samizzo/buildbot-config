#!/bin/bash

IPADDRESS="buildbot"
PORT=22
BB_USER="buildbot"
BB_HOME_DIR="/Users/$BB_USER/bb"
MASTER_DIR="$BB_HOME_DIR/master/master"

# Remove old scripts.
ssh -p $PORT $BB_USER@$IPADDRESS "cd $MASTER_DIR ; rm *.py *.pyc projects/*.py projects/*.pyc"

# Copy cfg and python scripts to build machine.
scp -P $PORT *.cfg *.py *.jade $BB_USER@$IPADDRESS:$MASTER_DIR

# Copy project scripts to build machine.
PROJECTS_DIR="$MASTER_DIR/projects"
ssh -p $PORT $BB_USER@$IPADDRESS "if [ ! -d $PROJECTS_DIR ] ; then mkdir $PROJECTS_DIR ; fi"
scp -P $PORT projects/*.py $BB_USER@$IPADDRESS:$PROJECTS_DIR

# Copy shell scripts to build machine.
scp -P $PORT *.sh *.plist $BB_USER@$IPADDRESS:$BB_HOME_DIR

# Run post-deploy setup.
ssh -p $PORT $BB_USER@$IPADDRESS "cd $BB_HOME_DIR ; sh setup.sh"
