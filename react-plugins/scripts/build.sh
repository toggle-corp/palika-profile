#!/bin/sh -x

echo '>> [Running] Build react-plugins'
cd /code/
yarn install && yarn build
