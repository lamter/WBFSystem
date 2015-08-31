# -*- coding: utf-8 -*-
"""
Created on 2015-08-31

@author: Shawn

"""
import traceback
import signal

import web
import gevent
from gevent.pool import Pool

import mygreenlet


SHUT_DOWN_SIGN = [
    signal.SIGQUIT,     # kill 信号
    signal.SIGINT,      # 键盘信号
]


def getShutDown():

    for sign in SHUT_DOWN_SIGN:
        ''' 关服信号 '''
        gevent.signal(sign, shutdown)




def shutdown():
    """
    关服时要做的事情
    """

    gls = [gl for gl in web.pool.greenlets]

    ''' 结束所有并发 '''
    try:
        web.pool.kill()
    except:
        traceback.print_exc()

    ''' 关闭 wsgi server 服务 '''
    web.wsgiServer.close()


    for gl in gls:
        if not gl.successful():
            print '================================'
            print 'started->', gl.started
            print 'ready()->', gl.ready()
            print 'successful()->', gl.successful()
            print 'value->', gl.value
            print 'exception->', gl.exception


if __name__ == '__main__':
    def run_forever():
        import paramiko
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect('123.59.44.14', 22, 'bpsg')

        cmd = 'ls'

        stdin, stdout, stderr = ssh.exec_command(cmd)

        print stdout.readlines()
        print ''.join(stderr.readlines())

        ssh.close()
        gevent.sleep(1000)


    pool = Pool(10)

    gevent.signal(signal.SIGQUIT, pool.kill)
    gevent.signal(signal.SIGINT, pool.kill)

    thread = pool.spawn(run_forever)

    pool.join(raise_error=True)
