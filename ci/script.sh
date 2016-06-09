#!/bin/bash
set -e -x
os.chdir('..')
nosetests -v --with-xcoverage --cover-package=convertbng --cover-tests


if [[ "$DOCKER_BUILD" == "TRUE" ]]; then
    docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/ci/build_wheel.sh
    pwd
    ls
    ls wheelhouse/
fi
