#!/bin/bash

echo
echo "Setting up buildbot.."
echo "Current user is $USER"

cd ~/bb

echo "Current directory is `pwd`"

# Ensure that all shell scripts are executable.
chmod u+x *.sh

LAUNCHAGENTS_DIR="/Users/$USER/Library/LaunchAgents"

# Create the launchctl directory on the build machine if it doesn't exist.
mkdir -p LAUNCHAGENTS_DIR

# Copy the plist to the launchctl directory.
cp net.buildbot.plist LAUNCHAGENTS_DIR

./stop-buildbot.sh

# Unload and reload the plist, which will start the buildbot.
launchctl unload LAUNCHAGENTS_DIR/net.buildbot.plist
launchctl load LAUNCHAGENTS_DIR/net.buildbot.plist
