#!/bin/bash
set -e -x
ls
if [[ "$DOCKER_BUILD" == "TRUE" ]]; then
    docker pull $DOCKER_IMAGE
fi
sudo pip install pip --upgrade
sudo pip install --install-option="--no-cython-compile" cython
sudo pip install numpy
sudo pip install python-coveralls
sudo pip install nosexcover
sudo pip install -e /home/travis/build/urschrei/setup.py
