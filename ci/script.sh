#!/bin/bash
set -e -x
ls $HOME/build/urschrei/convertbng/convertbng

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    cd $HOME/build/urschrei/convertbng && source venv/bin/activate
fi

# run the tests!
cd $HOME/build/urschrei/convertbng && nosetests -v --with-xcoverage --cover-package=convertbng --cover-tests

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker pull $DOCKER_IMAGE
    docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/ci/build_wheel.sh
    ls wheelhouse/
fi

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    pwd
    python setup.py bdist_wheel
    cp $HOME/build/urschrei/convertbng/dist/*.whl wheelhouse
fi
ls wheelhouse
