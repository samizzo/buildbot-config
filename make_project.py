# -*- python -*-
# ex: set filetype=python:

from dynamic_stages import *
from buildbot.plugins import *

def IsCleanBuild(step):
    return step.build.getProperties().has_key('clean') and step.build.getProperty('clean')

class MakeProject():
    def __init__(self, c, gitUrl, projectName, platforms, buildConfigs, pollInterval, nightlyHour, nightlyMinute):

        builderNames = [ projectName + '-' + b for b in platforms ]
        workDir = 'gitpoller-workdir-' + projectName
        forceSchedulerName = projectName + '-force'
        nightlySchedulerName = projectName + '-nightly'

        # We poll for changes. We can't use push notification because the server is behind a firewall.
        c['change_source'].append(changes.GitPoller(
            gitUrl,
            usetimestamps = False,
            workdir = workDir, branches = ['master'],
            project = projectName,
            pollInterval = pollInterval))

        # When there are changes available, we will build the master branch.
        c['schedulers'].append(schedulers.SingleBranchScheduler(
            name = projectName,
            change_filter = util.ChangeFilter(branch = 'master', project = projectName),
            treeStableTimer = 10,
            properties = {
                'clean': False,
                'distribution_build': False,
                'build_config': buildConfigs[0]
            },
            builderNames = builderNames))

        # Add a force build scheduler.
        c['schedulers'].append(schedulers.ForceScheduler(
            name = forceSchedulerName,
            buttonName = 'Force',
            label = 'Force build',
            properties = [
                util.NestedParameter(name = '', label = 'Build Options', layout = 'vertical', fields = [
                    util.BooleanParameter(name = 'clean', default = False, label = 'Clean build'),
                    util.BooleanParameter(name = 'distribution_build', default = False, label = 'Distribution build'),
                    util.ChoiceStringParameter(name = 'build_config', label = 'Build Config', choices = buildConfigs, default = buildConfigs[0])
                ])
            ],
            builderNames = builderNames))

        # Add a nightly clean scheduler.
        c['schedulers'].append(schedulers.Nightly(
            name = nightlySchedulerName,
            hour = nightlyHour,
            minute = nightlyMinute,
            properties = {
                'clean': True,
                'distribution_build': False,
                'build_config': buildConfigs[0]
            },
            change_filter = util.ChangeFilter(branch = 'master', project = projectName),
            builderNames = builderNames))

        # Add a builder for each build platform specified.
        for i in range(0, len(platforms)):
            # Set up the build steps.
            factory = util.BuildFactory()

            # First remove the build directory if we are doing a clean build.
            factory.addStep(steps.RemoveDirectory(dir = 'build', doStepIf = IsCleanBuild))

            # Check out the source.
            factory.addStep(steps.Git(
                repourl = gitUrl,
                mode = 'incremental',
                logEnviron = False))

            # Next generate the build stages to build for the specified platform.
            stages = GenerateStagesCommand(
                platforms[i],
                name = 'Generate build stages',
                description = 'Generate build stages',
                logEnviron = False,
                command = [ 'python', './build.py', '--list-stages', platforms[i] ],
                haltOnFailure = True,
                env = {
                    'GOT_REVISION': util.Property('got_revision'),
                    'DISTRIBUTION_BUILD': util.Interpolate('%(prop:distribution_build)s'),
                    'BUILD_NUMBER': util.Interpolate('%(prop:buildnumber)s'),
                    'BUILD_CONFIG': util.Interpolate('%(prop:build_config)s'),
                    'BUILD_URL': util.URLForBuild
                })
            factory.addStep(stages)

            c['builders'].append(
                util.BuilderConfig(name = builderNames[i],
                  workernames = [ 'worker' ],
                  factory = factory))

