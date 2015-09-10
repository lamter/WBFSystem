#!/bin/bash
# start_server.sh

source $HOME/.bash_profile
workon WEBFSystem


cd ../www

python main.py bpsgs &

# 启动状态检查
ps -ef|grep bpsgs
#tail -f ./log/wbfs.log
