paraSSH
=======
Author: chris.hill
Email: im.weittor#gmail.com
Date: 20140528


##简介
clusterCMD.py    ---    远程执行用户命令
clusterDeliver.py   --- 远程传输文件


##依赖包
需要安装python的paramiko模块

安装方法：
```
sudo apt-get install python-paramiko
yum install python-paramiko
```

##使用方法
###编辑默认配置文件config.ini
也可以自己指定配置文件。

配置文件格式如下：
```
ip地址          用户名      密码
192.168.1.1     root       weittor.com
192.168.100.1   root       123456
```

###clusterCMD使用方法
* 使用fdping.py脚本判断一下文件内的ip地址是否全部可达。

执行：
```
python fdping.py
```
若无任何输出，则说明IP地址全部可达。

* 使用clusterCMD.py脚本可对配置文件内的服务器执行远程操作。

需要注意有三种认证方式可选：
a. 需要填写用户名和密码，默认为该方式。若不设置，则默认采用该方式认证。需要正确配置config.ini配置文件内的用户名跟密码选项。    
b. pkey认证，私钥认证。需要提供私钥文件。   
c. keyfile认证，包含私钥信息认证文件。   

####举例

用户名和密码认证方式，执行date命令
```
python clusterCMD.py --command='date'
```

pkey认证    
```
python clusterCMD.py --command='date' --auth=pkey
```

keyfile认证    
```
python clusterCMD.py --command='date' --auth=keyfile
```


###clusterDeliver使用方法
使用clusterDeliver.py可以远程传输文件

需要注意有两种认证方式可选：

a. 需要填写用户名和密码，默认为该方式。若不设置，则默认采用该方式认证。需要正确配置config.ini配置文件内的用户名跟密码选项。     
b. pkey认证，私钥认证。需要提供私钥文件。  

####举例

用户名和密码认证方式。
```
python clusterDeliver.py --source='/tmp/1.txt' --dest='/tmp/2.txt'
```

pkey认证
```
python clusterDeliver.py --auth=pkey --source='/tmp/1.txt' --dest='/tmp/2.txt'
```










