#!/bin/bash
# start_server.sh

cd ../www
# uwsgi --http :8080 -p 1 -w main -T --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log
uwsgi --gevent 100 --gevent-monkey-patch --http :8080 -M  -p 1 --wsgi-file myapp.py --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log
ps -ef|grep uwsgi