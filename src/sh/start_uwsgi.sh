#!/bin/bash
# start_server.sh

cd ../www

#uwsgi --http :8080 -p 1 -w main -T --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log
#ps -ef|grep uwsgi

# 线程并发
# uwsgi --http :8080 -p 1 -w main -T --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log --threads 100

# gevent 并发
uwsgi --gevent 100 --gevent-monkey-patch --http :8080 -M  -p 1 --wsgi-file main.py --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log
uwsgi --loop gevent --async 100 --gevent-monkey-patch --socket :8080 --wsgi-file main.py --pyargv "--dbhost localhost --dbp 8911 --db 1 " -d ./log/wbfs.log

# 启动状态检查
ps -ef|grep uwsgi
tail -f ./log/wbfs.log
