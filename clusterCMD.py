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




import sys
import os
import optparse 
import time
import threading
from libs import paraTools


try:
    from paramiko import SSHClient, SFTPClient, Transport, RSAKey, AutoAddPolicy
except:
    print "You need module paramiko."




def mkpasswdAuthThread(configfile,command):
    '''
    @note: 使用password验证连接
    '''
    config = open(configfile,'r')
    threads= []

    for line in config:
        if not line.strip():
            break
        else:
            ip = line.split()[0].strip()
            username = line.split()[1].strip()
            password = line.split()[2].strip()
            print ip
            print username
            print password
            threads.append(threading.Thread(target=paraTools.passwdAuthCMD,args=(ip, username, password, command)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    config.close()

def mkkeyfileAuthCMD(configfile, key_file, command):
    '''
    @note: 使用keyfile方式验证连接
    '''
    config = open(configfile,'r')
    threads= []

    for line in config:
        if not line.strip():
            break
        else:
            ip = line.split()[0].strip()
            username = line.split()[1].strip()
            print ip
            print username
            threads.append(threading.Thread(target=paraTools.keyfileAuthCMD,args=(ip, username, key_file, command)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    config.close()

def mkpkeyAuthCMD(configfile, pkey_file, command):
    '''
    @note: 使用pkey方式验证连接
    '''
    config = open(configfile,'r')
    threads= []
    pkeyFile = pkey_file
    command = command

    for line in config:
        if not line.strip():
            break
        else:
            ip = line.split()[0].strip()
            username = line.split()[1].strip()
            print ip
            print username
            threads.append(threading.Thread(target=paraTools.pkeyAuthCMD,args=(ip, username, pkey_file, command)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    config.close()


def main():
    '''
    @note: 主函数进程
    '''
    USAGE = 'python %prog [--config=config.ini] --command="CMD"  [--auth=<passwd|pkey|keyfile>] [--pkey=pkey] [--keyfile=keyfile]\n\nExample: %prog --config=config.ini --command="ls" --auth=pkey  --pkey="/root/id_rsa"'
    VERSION = '%prog 1.0'
    DESC = u"""This is a cluster tools to exec ssh commands.The minimum version of python required
 was 2.3."""
    parser = optparse.OptionParser(usage=USAGE, version=VERSION, description=DESC)
    parser.add_option('-f', '--config', default='config.ini',help='The main config file.Default is config.ini.')
    parser.add_option('-c', '--command', help='The command that you want to exec.')
    parser.add_option('-a', '--auth', help='The authorized method you can select is [passwd|pkey|keyfile].Default is passwd.')
    parser.add_option('-p', '--pkey', default='~/.ssh/id_rsa', help='If  the authorized method you set  is pkey, you can change the pkey file.Default is ~/.ssh/id_rsa.')
    parser.add_option('-k', '--keyfile', default='~/.ssh/id_rsa', help='If  the authorized method you set is keyfile, you can change the keyfile.Default is ~/.ssh/id_rsa.')

    opts, args= parser.parse_args()

    if opts.command is None:
        sys.exit('ERROR:  All parameters followed were required: --command.\n\nUse -h to get more help.')

    print time.ctime()
    if not os.path.exists(opts.config):
        print "You must change the config.ini first."
        sys.exit(1)


    if opts.config:
        config = os.getcwd() + "/" + opts.config
    else:
        config = os.getcwd() + "/config.ini"
        print config


    if opts.auth == 'pkey' and opts.pkey is not None:
        pkey = os.path.expanduser(opts.pkey)
        print pkey
        mkpkeyAuthCMD(config, pkey, opts.command)
    elif opts.auth == 'keyfile' and opts.keyfile is not None:
        keyfile = os.path.expanduser(opts.keyfile)
        print keyfile
        mkkeyfileAuthCMD(config, keyfile, opts.command)
    else:
        mkpasswdAuthThread(config, opts.command)



if __name__ == "__main__":
    main()


