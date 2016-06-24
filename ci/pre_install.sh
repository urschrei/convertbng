#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    sudo pip install pip --upgrade
    sudo pip install nosexcover
    sudo pip install python-coveralls
    sudo pip install requests
    sudo python ci/pre_install.py
fi
