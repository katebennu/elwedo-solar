#!/bin/bash

REMOTE_HOST=elwedo@elwedo.kbennu.com
REMOTE_DIR=/home/elwedo/solarpilot

rsync -a --exclude='.git/' . ${REMOTE_HOST}:${REMOTE_DIR}
ssh ${REMOTE_HOST} "\
    cd ${REMOTE_DIR};\
    docker-compose stop web;\
    docker-compose rm -f web;\
    docker-compose build;\
    docker-compose create web;\
    docker-compose start web;\
    docker-compose up -d --no-recreate postgres"