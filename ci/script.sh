#!/bin/bash
set -e -x

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    source venv/bin/activate
fi
# run the tests!
nosetests -v --with-xcoverage --cover-package=convertbng --cover-tests

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    mkdir -p $HOME/build/urschrei/convertbng/wheelhouse
    # clean up
    sudo rm convertbng/cutil.so
    sudo rm -rf convertbng.egg-info
    sudo rm -rf build
    sudo rm -f *.pyc
    sudo rm -f convertbng/*.pyc

    docker pull $DOCKER_IMAGE
    docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/ci/build_wheel.sh
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    mkdir -p $HOME/build/urschrei/convertbng/wheelhouse
    python setup.py bdist_wheel
    cp dist/*.whl $HOME/build/urschrei/convertbng/wheelhouse
fi
