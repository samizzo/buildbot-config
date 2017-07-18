# -*- python -*-
# ex: set filetype=python:

from buildbot.plugins import *
from buildbot.process import buildstep, logobserver
from twisted.internet import defer
import json
from os.path import basename

# This class dynamically generates a list of build steps by running a bash script.
class GenerateStagesCommand(buildstep.ShellMixin, steps.BuildStep):

    def __init__(self, platform, **kwargs):
        self.platform = platform
        kwargs = self.setupShellMixin(kwargs)
        steps.BuildStep.__init__(self, **kwargs)
        self.observer = logobserver.BufferLogObserver()
        self.addLogObserver('stdio', self.observer)

    # Parses a json string into an object and converts unicode strings into regular strings.
    def json_loads_byteified(self, json_text):
        return self._byteify(json.loads(json_text, object_hook=self._byteify), ignore_dicts=True)

    def _byteify(self, data, ignore_dicts = False):
        if isinstance(data, unicode):
            return data.encode('utf-8')
        if isinstance(data, list):
            return [ self._byteify(item, ignore_dicts = True) for item in data ]
        if isinstance(data, dict) and not ignore_dicts:
            return {
                self._byteify(key, ignore_dicts = True): self._byteify(value, ignore_dicts = True)
                for key, value in data.iteritems()
            }
        return data

    # Extract a list of stages from the stdout.
    def extract_stages(self, stdout):
        stages = []
        for line in stdout.split('\n'):
            if len(line) == 0:
                continue
            stage = self.json_loads_byteified(line)
            if 'stage' in stage:
                stages.append(stage)
        return stages

    @defer.inlineCallbacks
    def run(self):
        # Run './build.py --list-stages' to generate the list of stages.
        cmd = yield self.makeRemoteShellCommand()
        yield self.runCommand(cmd)

        result = cmd.results()
        if result == util.SUCCESS:
            # Create a ShellCommand for each stage and add them to the build.
            stages = []
            for stage in self.extract_stages(self.observer.getStdout()):
                stageName = stage['stage']
                args = dict(
                    name = stageName,
                    logEnviron = False,
                    description = stageName,
                    command = [ 'python', './build.py', '--run-stage', stageName, self.platform ],
                    env = {
                        'GOT_REVISION': util.Property('got_revision'),
                        'DISTRIBUTION_BUILD': util.Interpolate('%(prop:distribution_build)s'),
                        'BUILD_NUMBER': util.Interpolate('%(prop:buildnumber)s'),
                        'BUILD_CONFIG': util.Interpolate('%(prop:build_config)s'),
                        'BUILD_URL': util.URLForBuild
                    },
                    haltOnFailure = True
                )
                if 'timeout' in stage:
                    args['timeout'] = stage['timeout']
                if 'logfile' in stage:
                    logpath = stage['logfile']
                    logname = basename(logpath)
                    args['logfiles'] = { logname: logpath }
                if 'description' in stage:
                    args['description'] = stage['description']
                    args['descriptionDone'] = stage['description']
                    args['name'] = stage['description']
                newStage = steps.ShellCommand(**args)
                stages.append(newStage)
            self.build.addStepsAfterCurrentStep(stages)

        defer.returnValue(result)

