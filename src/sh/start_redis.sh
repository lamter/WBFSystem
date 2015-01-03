#!/bin/bash
# redis_start.sh

echo $1

if [ "$1" = "-r" ]
then
    echo "重启redis..."
    sh redis_stop.sh
fi

cd ../redis/bin
if ! [ -f `pwd`/redis.pid ]
then
    echo 当前路径: `pwd`
    echo "启动新的redis服务器..."
    redis-server redis.conf
else
    echo "redis服务已经启动..."
fi

ps -ef|grep redis-server