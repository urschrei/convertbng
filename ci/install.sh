#!/bin/bash
echo $HOME
set -e -x
if [[ "$DOCKER_BUILD" == "TRUE" ]]; then
    docker pull $DOCKER_IMAGE
fi
sudo pip install pip --upgrade
sudo pip install --install-option="--no-cython-compile" cython
sudo pip install numpy
sudo pip install python-coveralls
sudo pip install nosexcover
cd $HOME/build/urschrei/convertbng && sudo pip install -e .
