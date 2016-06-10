#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker pull $DOCKER_IMAGE
    sudo pip install pip --upgrade
    sudo pip install --install-option="--no-cython-compile" cython
    sudo pip install numpy
    sudo pip install python-coveralls
    sudo pip install nosexcover
    echo "Linux!"
    ls $HOME/build/urschrei/convertbng
    ls $HOME/build/urschrei/convertbng/convertbng
    sudo pip install -e $HOME/build/urschrei/convertbng
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    source $HOME/build/urschrei/convertbng/venv/bin/activate
    pip install pip --upgrade
    pip install --install-option="--no-cython-compile" cython
    pip install numpy
    pip install python-coveralls
    pip install nosexcover
    echo "OSX!"
    mv $HOME/build/urschrei/convertbng/convertbng/convertbng/liblonlat_bng.dylib $HOME/build/urschrei/convertbng/convertbng/
    rm -rf $HOME/build/urschrei/convertbng/convertbng/convertbng/
    ls $HOME/build/urschrei/convertbng
    ls $HOME/build/urschrei/convertbng/convertbng
    pip install -e $HOME/build/urschrei/convertbng
    # otool -L $HOME/build/urschrei/convertbng/convertbng/liblonlat_bng.dylib
fi
