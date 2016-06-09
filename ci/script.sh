#!/bin/bash
set -e -x
if [[ "$DOCKER_BUILD" == "TRUE" ]]; then
    docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/ci/build_wheel.sh
    ls wheelhouse/
fi
