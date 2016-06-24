#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    sudo pip install pip --upgrade
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    # install OSX
    source ci/travis_osx_steps.sh
fi
