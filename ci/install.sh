#!/bin/bash
set -e -x
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    sudo pip install pip --upgrade
    sudo pip install --install-option="--no-cython-compile" cython
    sudo pip install python-coveralls
    sudo pip install nosexcover
    sudo pip install -e $HOME/build/urschrei/convertbng -v
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    pip install -r dev-requirements.txt
    python ci/pre_install.py
    pip install --install-option="--no-cython-compile" cython
    pip install python-coveralls
    pip install nosexcover
    # install_name_tool -change /Users/travis/build/urschrei/lonlat_bng/target/x86_64-apple-darwin/release/liblonlat_bng.dylib @loader_path/liblonlat_bng.dylib $HOME/build/urschrei/convertbng/convertbng/cutil.so
fi
