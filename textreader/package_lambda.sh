#!/bin/bash -e

BASEDIR=`dirname $0`
. ~/.bash_profile


source ~/virtualenvs/textreadermini/bin/activate
python setup.py install
cp -r `find ~/virtualenvs/textreadermini/ -type d -name site-packages`/.  build/deploy
pushd build/deploy
zip -r deploy.zip .
popd
mv build/deploy/deploy.zip ./deploy_lambda.zip
source ~/virtualenvs/textreader/bin/activate
