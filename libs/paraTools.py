#!/usr/bin/env python
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
try:
    from paramiko import SSHClient, SFTPClient, Transport,  RSAKey, AutoAddPolicy
except:
    print "You need module paramiko."






def passwdAuthCMD(node, username, password, command):
    s = SSHClient()
    s.set_missing_host_key_policy(AutoAddPolicy())
    s.connect(node, username=username, password=password)
    print "The server accept the username %s"% username
    stdin, stdout, stderr = s.exec_command(command)
    print "The server exec the command %s"% command 
    print stdout.read().strip()
    s.close()

def keyfileAuthCMD(node, username, key_file, command):
    s = SSHClient()
    s.set_missing_host_key_policy(AutoAddPolicy())
    s.connect(node, username=username, key_filename=key_file)
    print "The server accept the username %s"% username
    stdin, stdout, stderr = s.exec_command(command)
    print "The server exec the command %s"% command 
    print stdout.read().strip()
    s.close()

def pkeyAuthCMD(node, username, pkey_file, command):
    s = SSHClient()
    s.set_missing_host_key_policy(AutoAddPolicy())
    pkey_file = pkey_file
    key = RSAKey.from_private_key_file(pkey_file)
    s.connect(node, username=username, pkey=key, look_for_keys=False)
    print "The server accept the username %s"% username
    s.exec_command(command)
    print "The server exec the command %s"% command 
    s.close()

def passwdAuthDeliver(node, username, password, source, dest):
    t = Transport((node, 22))
    t.connect(username=username, password=password)
    s = SFTPClient.from_transport(t)
    s.put(source, dest)
    t.close()

def pkeyAuthDeliver(node, username, pkey_file, source, dest):
    t = Transport((node, 22))
    pkey_file = pkey_file
    key = RSAKey.from_private_key_file(pkey_file)
    t.connect(username=username, pkey=key)
    s = SFTPClient.from_transport(t)
    s.put(source, dest)
    t.close()



