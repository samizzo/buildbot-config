@echo off
set IPADDRESS=buildbot
set PORT=22
set BB_USER=buildbot
set PASSWORD=password
set BB_HOME_DIR=/Users/%BB_USER%/bb
set MASTER_DIR=%BB_HOME_DIR%/master/master

rem Remove old scripts.
plink -P %PORT% -pw %PASSWORD% %BB_USER%@%IPADDRESS% "cd %MASTER_DIR% ; rm *.py *.pyc projects/*.py projects/*.pyc"

rem Copy cfg and python scripts to build machine.
pscp -P %PORT% -pw %PASSWORD% *.cfg *.py *.jade %BB_USER%@%IPADDRESS%:%MASTER_DIR%

rem Copy project scripts to build machine.
set PROJECTS_DIR=%MASTER_DIR%/projects
plink -P %PORT% -pw %PASSWORD% %BB_USER%@%IPADDRESS% "if [ ! -d %PROJECTS_DIR% ] ; then mkdir %PROJECTS_DIR% ; fi"
pscp -P %PORT% -pw %PASSWORD% projects/*.py %BB_USER%@%IPADDRESS%:%PROJECTS_DIR%

rem Copy shell scripts to build machine.
pscp -P %PORT% -pw %PASSWORD% *.sh *.plist %BB_USER%@%IPADDRESS%:%BB_HOME_DIR%

rem Run post-deploy setup.
plink -P %PORT% -pw %PASSWORD% %BB_USER%@%IPADDRESS% "cd %BB_HOME_DIR% ; sh setup.sh"
