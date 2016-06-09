#!/bin/bash
set -e -x
ls ../convertbng/convertbng
nosetests -v --with-xcoverage --cover-package=convertbng --cover-tests


if [[ "$DOCKER_BUILD" == "TRUE" ]]; then
    docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/ci/build_wheel.sh
    ls wheelhouse/
fi
