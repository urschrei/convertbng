#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    sudo pip install pip --upgrade
    sudo pip install --install-option="--no-cython-compile" cython
    sudo pip install numpy
    sudo pip install python-coveralls
    sudo pip install nosexcover
    echo "Linux!"
    ls $HOME/build/urschrei/convertbng
    ls $HOME/build/urschrei/convertbng/convertbng
    sudo pip install -e $HOME/build/urschrei/convertbng -v
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    source $HOME/build/urschrei/convertbng/venv/bin/activate
    pip install pip --upgrade
    pip install --install-option="--no-cython-compile" cython
    pip install numpy
    pip install python-coveralls
    pip install nosexcover
    echo "OSX!"
    pwd
    cd $HOME/build/urschrei/convertbng && install_name_tool -change /Users/travis/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/liblonlat_bng.dylib @loader_path/liblonlat_bng.dylib convertbng/cutil.so
    pip install -e $HOME/build/urschrei/convertbng -v
    otool -L $HOME/build/urschrei/convertbng/convertbng/liblonlat_bng.dylib
fi
