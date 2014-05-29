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







def mkpasswdAuthDeliver(configfile, source, dest):
    '''
    @note: 使用password验证连接，传送文件
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
            threads.append(threading.Thread(target=paraTools.passwdAuthDeliver, args=(ip, username, password, source, dest)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    config.close()


def mkpkeyAuthDeliver(configfile, pkey_file, source, dest):
    '''
    @note: 使用pkey验证连接，传送文件
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
            threads.append(threading.Thread(target=paraTools.pkeyAuthDeliver, args=(ip, username, pkey_file, source, dest)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    config.close()

def main():
    '''
    @note: 主函数进程
    '''
    USAGE = 'python %prog [--config=config.ini] [--auth=<passwd|pkey>] [--pkey=pkey] source=source_file dest=dest_file \n\nExample: %prog --config=config.ini  --auth=pkey  source="/tmp/1.txt" dest="/tmp/2.txt"'
    VERSION = '%prog 1.0'
    DESC = u"""This is a cluster tools to deliver files.The minimum version of python required
 was 2.3."""
    parser = optparse.OptionParser(usage=USAGE, version=VERSION, description=DESC)
    parser.add_option('-f', '--config', default='config.ini',help='The main config file.Default is config.ini.')
    parser.add_option('-a', '--auth', help='The authorized method you can select is [passwd|pkey|keyfile].Default is passwd.')
    parser.add_option('-p', '--pkey', default='~/.ssh/id_rsa', help='If  the authorized method you set  is pkey, you can change the pkey file.Default is ~/.ssh/id_rsa.')
    parser.add_option('-s', '--source', help='You must set the source filename.')
    parser.add_option('-d', '--dest', help='You must set the dest filename.')

    opts, args= parser.parse_args()

    if opts.source is None or opts.dest is None:
        sys.exit('ERROR:  All parameters followed were required: --source & --dest.\n\nUse -h to get more help.')

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
        mkpkeyAuthDeliver(config, pkey, opts.source, opts.dest)
    else:
        mkpasswdAuthDeliver(config, opts.source, opts.dest)



if __name__ == "__main__":
    main()


