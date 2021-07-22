#!/bin/sh

target_path=./technest
target_name=contreras-alberto-technest-challenge.zip

rm -rf ${target_path} ${target_name}
mkdir ${target_path}
cp -vR app data production static templates .dockerignore docker-compose* \
    Dockerfile Makefile README.md requirements* TODO ${target_path}

zip -r ${target_name} ${target_path}/*
zip -sf ${target_name}
