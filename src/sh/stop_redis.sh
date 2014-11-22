#!/bin/bash

cd ../redis/bin
if [ -f redis.pid ]
then
    echo "关闭redis模块..."
    kill `cat redis.pid`
else
    echo "redis模块已经被关闭了..."
fi

# 如果.pid文件没有删除，要删除掉
if [ -f redis.pid ]
then
    echo "清除参与的redis.pid文件..."
    rm `pwd`/redis.pid
fi