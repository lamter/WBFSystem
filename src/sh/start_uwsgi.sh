#!/bin/bash
# start_server.sh

cd ../www
uwsgi --http :8080 -p 1 -w main -T --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log
ps -ef|grep uwsgi