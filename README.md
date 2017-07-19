# buildbot server config

This repository is a set of scripts to configure and run a buildbot instance. They are
designed to be used on a Mac for building iOS and Android applications, but they should
be able to be used on any UNIX-like operating system with Python. They probably won't
work under Windows.

The scripts assume you have a user called 'buildbot' on your Mac build machine.

## Basic installation

1. Copy *initial_setup.sh* and *install_buildbot.sh* to a directory called `bb` in the
   home directory of your buildbot user.
2. Run *initial_setup.sh*. This will install homebrew, python2, pip, virtualenv,
   python-dateutil, and xcpretty.
3. Run *install_buildbot.sh*. This will install master and worker instances of buildbot
   into `$HOME/bb/master` and `$HOME/bb/worker`.
4. Create projects in the `projects` directory.
5. Deploy project changes to the server using `deploy.bat` or `deploy.sh`.

## Overview

This buildbot configuration is set up to automatically load all modules in the `projects`
subdirectory. You can add your project configurations to that directory by following the
sample project, then deploy the updated scripts to the server and restart buildbot. The
new projects will be loaded automatically by the buildbot master config.

Projects defined in this way will dynamically generate buildbot build stages by running
a script called `build.py` in the project's root directory after it has been checked out
from source control. The `build.py` script is responsible for telling the buildbot server
the names of the build stages it can handle, and also for actually building those stages.

This setup provides:

  * A nightly build which does a full clean and rebuild.
  * A continuous build which builds as changes are checked in (via polling, since your
    build server is probably behind a firewall).
  * A force build which allows you to make a specific build with some specific settings
    (e.g. choose a build config and whether you want to do a clean build).

## Projects

In the `projects` directory in this repository there is a file called `sample_project.py`.
You can use this as a basis for building your own project configurations.

Here is an example of a project configuration:

```
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
```

This will configure:

  * Builders for all the specified platforms.
  * For each platform, a nightly builder and a continuous builder.

The project's build script `build.py` has access to several build parameters that can be
set differently depending on the type of build which is running:

  * A build config value (e.g. "debug", "release", "final").
  * A boolean value indicating whether to do a clean build.
  * A boolean value indicating whether to do a distribution build (this can be used by
    build scripts for any purpose, e.g. upload to iTunes Connect).

The nightly builder and continuous builder set "distribution build" to false and select the
first defined build config. The continuous builder sets "clean" to false and the nightly builder
sets it to "true". When force building a project in the buildbot web dashboard, these options
can be set separately.

Each build step for a project is passed the following additional environment variables:

  * GOT_REVISION - the source control revision that is being built.
  * DISTRIBUTION_BUILD - a boolean value indicating if the distribution build flag is set.
  * BUILD_NUMBER - the number of the current build.
  * BUILD_CONFIG - the configuration name for the current build.
  * BUILD_URL - the url to the status page for the current build.
