#!/bin/bash

REMOTE_HOST=elwedo@elwedo.kbennu.com
REMOTE_DIR=/home/elwedo/solarilot

rsync -a --exclude='.git/' . ${REMOTE_HOST}:${REMOTE_DIR}
ssh ${REMOTE_HOST} "cd ${REMOTE_DIR}; docker-compose stop web; docker-compose build; docker-compose up -d --no-recreate postgres"