#!/bin/bash
# start_server.sh

cd ../www
uwsgi -s 127.0.0.1:80 -w main -T --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log
ps -ef|grep uwsgi