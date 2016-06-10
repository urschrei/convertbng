#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker pull $DOCKER_IMAGE
    sudo pip install pip --upgrade
    sudo pip install --install-option="--no-cython-compile" cython
    sudo pip install numpy
    sudo pip install python-coveralls
    sudo pip install nosexcover
    cd $HOME/build/urschrei/convertbng && sudo pip install -e .
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    echo "OSX!"
    source $HOME/build/urschrei/convertbng/venv/bin/activate
    pip install pip --upgrade
    # pip install --install-option="--no-cython-compile" cython
    pip install numpy
    pip install python-coveralls
    pip install nosexcover
    cd $HOME/build/urschrei/convertbng && pip install -e .
    # otool -L $HOME/build/urschrei/convertbng/convertbng/liblonlat_bng.dylib
    # mkdir -p $HOME/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/
    # cp $HOME/build/urschrei/convertbng/convertbng/liblonlat_bng.dylib $HOME/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/ 
fi

