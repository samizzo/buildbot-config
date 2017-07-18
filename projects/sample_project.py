# -*- python -*-
# ex: set filetype=python:

from make_project import *
import __builtin__

# Name of the project!
PROJECT_NAME = 'sample_project'

# Url for the project repository. Note: only git is currently supported!
URL = 'git@bitbucket.org:username/sample_project.git'

# Time in seconds to poll for changes.
POLL_INTERVAL = 300

# Nightly build time.
NIGHTLY_HOUR = 23
NIGHTLY_MINUTE = 50

# Platforms we want to build.
PLATFORMS = [ 'ios', 'android', 'tvos' ]

# Build configs we want to build.
BUILD_CONFIGS = [ 'Release', 'Profile', 'Final' ]

# And set it up!
MakeProject(__builtin__.BuildmasterConfig, URL, PROJECT_NAME, PLATFORMS, BUILD_CONFIGS, POLL_INTERVAL, NIGHTLY_HOUR, NIGHTLY_MINUTE)
