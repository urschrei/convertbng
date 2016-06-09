#!/bin/bash
set -e -x
pwd
ls
ls convertbng
if [[ "$DOCKER_BUILD" == "TRUE" ]]; then
    docker pull $DOCKER_IMAGE
fi
sudo pip install pip --upgrade
sudo pip install --install-option="--no-cython-compile" cython
sudo pip install numpy
sudo pip install python-coveralls
sudo pip install nosexcover
cd convertbng && sudo pip install .
