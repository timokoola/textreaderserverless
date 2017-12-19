#!/bin/bash -e

BASEDIR=`dirname $0`
VIRTUALENVS_ROOT="$HOME/.pyenv/versions/3.6.1/envs"
DEV_ENV="$VIRTUALENVS_ROOT/textreader"
DEPLOYMENT_ENV="$VIRTUALENVS_ROOT/textreadermini"
. ~/.bashrc


pyenv activate textreadermini
python setup.py install
cp -r `find ~/.pyenv/versions/3.6.1/envs/textreadermini/ -type d -name site-packages`/.  build/deploy
pushd build/deploy
zip -r deploy.zip .
popd
mv build/deploy/deploy.zip ./deploy_lambda.zip