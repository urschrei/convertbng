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
if [[ "$DOCKER_BUILD" != "TRUE" ]]; then
    mkdir -p $HOME/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/
    cp $HOME/build/urschrei/convertbng/convertbng/liblonlat_bng.dylib $HOME/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/ 
fi
/Users/travis/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/liblonlat_bng.dylib
cd $HOME/build/urschrei/convertbng && sudo pip install -e .
