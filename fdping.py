#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    @author: chris.hill , <im.weittor@gmail.com>
    @copyright: (C) 2014 weittor
    @license: GNU General Public License version 2.0 (GPLv2)
    @version: 0.1
    @contact:
    @var:
    @type:
    @param:
    @return:
    @rtype:
    @note:
    @attention:
    @bug:
    @warning:
    @see:
"""






import socket
import sys
import os
import re
import string
import threading
import time

def check_ip(addr):
    '''
    @note: 判断ip地址合法性
    @param 
    @return: 返回不正确的ip地址提示
    '''
    try:
        socket.inet_aton(addr)
    except socket.error:
        return "not ipv4 address"

def ipPing(server):
    '''
    @note: 使用ping判断主机是否存活
    @param server: 获取主机的ip地址
    @return: 返回主机是否存活的提示信息
    '''

    missInfo = re.compile(r"0 received")

    ipCheck = check_ip(server)
    if not ipCheck:
        pingCMD = os.popen("ping -c 2 -w 2 " + server,"r")
    else:
        print "IP %s is not correct!" % server
        sys.exit(1)
    while 1:
        line = pingCMD.readline()
        if not line:
            break;
        imiss = re.findall(missInfo, line)
        if imiss:
            print "Server %s not reachable. " % server

def mkThread():
    '''
    @note: 生成线程信息
    @param：无
    @return: 主机存活信息
    '''
    config = open('config.ini','r')
    threads= []

    for line in config:
        if not line.strip():
            break
        else:
            ip = line.split()[0].strip()
            print ip
            threads.append(threading.Thread(target=ipPing,args=(ip,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    config.close()




if __name__ == '__main__':
    '''
    @note: 通过ping工具，判断config.ini文件内的ip地址是否存活
    @return: 返回不可到达的ip地址列表。若全部可以ping通，则没有任何输出。
    '''


    print time.ctime()
    if not os.path.exists('config.ini'):
        print "You must change the config.ini first."
        sys.exit(1)
    mkThread()


