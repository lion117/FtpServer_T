# 前言
在windows下开发后台服务, 经常需要提供FTP服务, 以提供稳定的文件上传,下载服务.
windows作为一个成熟稳定的平台, 网上提供大量的收费,免费软件. 
经过一番调研之后, 发现多数软件都是直接面向用户的（带界面）,需要用户单独安装后才能使用. 对于开发者而言,并不优好. 

![image](http://note.youdao.com/yws/api/group/27115823/file/106686030?method=getImage&width=640&height=640&version=1&cstk=dWk145O9)

# 面向开发者FTP服务器要求
- 安全性
    - 要求提供用户名和密码登陆
    - 要求限制用户的读写管理权限
- 部署便捷性
    - 绿色版
    - 后台静默运行（无多余弹窗）
    - 可支持后台服务自启动
    - 可通过编程的方式配置FTP服务器参数,
        - 监听IP
        - 监听端口
        - 默认根目录
        - 允许多用户同时连接传输
        - 自动记录日志信息

- 稳定性
    - 能够长期稳定后台运行
    - 能够提供流量控制,连接数控制
- 跨平台,可支持windows, linux



# C++语言的困境
## C++语言的FTP服务器

笔者的服务器是基于Cplusplus开发的windows程序

1. 笔者最直接的反应是寻找一个知名的第三方的FTP服务器库作为基础起点. 但是经过一番google之后, 却失望的发现, 多数知名库都只提供FTP客户端的库(boost , poco)
2.  一些小的第三方FTP服务器不是性能不稳定, 就是功能缺陷.  
3.  网上有人建议自己撸一个FTP服务器,并提供简要的思路和代码. 但是考虑稳定性不足和可维护性, 笔者放弃了这条道路. 基于C++的语言的FTP服务器


## JAVA , C# 服务器
既然C++ 没有现成的FTP服务器, java和C#总是有的啊. 基本的功能都能很好的符合需求. 但是需要携带一个 jre 或者.net framework的环境包. 一个FTP功能,就比主程序功能还大. 太说不过去了. 此路不适合

## python生成exe方案
几经调查,笔者将目标锁定到python的**pyftpdlib**库上. 基本一下特点：
1. 接口简单,友好,容易上手
2. 功能丰富,可面向编程使用
3. 轻量级
4. 自带支持命令行启动FTP

考虑到python可以使用py2exe,将编译语言转换成exe文件执行. 体积上可以大大减小. 能够做到绿色版

# 基于python的FTP服务器
## 特点：
- 支持xp,win7,win8,win10,对系统环境变化不敏感
- 绿色,轻量级
- 功能丰富,可通过ini文件对服务器进行配置
- 可实现后台服务功能和后天静默启动

![image](http://note.youdao.com/yws/api/group/27115823/file/106686029?method=getImage&width=640&height=640&version=1&cstk=dWk145O9)

***话不多数, 放码出来***

### ini配置文件
```INI
[base]
anonymous = 1                       ;是否允许匿名登录
user = ITC                          ;用户名
password = ITC123                   ;密码
port = 2121                         ;侦听端口号
dir =  c://new/test/good            ;#默认路径
hided = 0                           ;是否隐藏当前窗口


[advanced]
max_connect =256                     ;同时最大允许连接数
permission = elradfmw                ;允许权限
autosetup = 1                        ;是否随机启动


;Read permissions:
;- "e" = change directory (CWD command)
;- "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
;- "r" = retrieve file from the server (RETR command)
;
;Write permissions:
;- "a" = append data to an existing file (APPE command)
;- "d" = delete file or directory (DELE, RMD commands)
;- "f" = rename file or directory (RNFR, RNTO commands)
;- "m" = create directory (MKD command)
;- "w" = store a file to the server (STOR, STOU commands)
;- "M" = change file mode (SITE CHMOD command)

```

### ftp模块

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os, sys
import ctypes
sys.path.append(os.path.abspath('..'))
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from Logger import  logger
import platform





g_user =u"ITC"
g_password =u"ITC123"
g_dir =u"c:"
g_port =2121
g_banonymous = False
g_hided = False

# advanced feature
g_max_connect=256
g_permission = "elradfmw"                #允许权限
g_bautostartup = 0                         #是否随机启动



def read_config():
    global g_user
    global g_password
    global g_dir
    global g_port
    global g_banonymous
    global g_hided

    global g_bautostartup
    global g_max_connect
    global g_permission

    try:
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.join(os.getcwd(), "FtpConfig.ini"))

        if cf.has_option("base","user"):
            g_user = cf.get("base", "user").decode("GBK")
        if cf.has_option("base","password"):
            g_password = cf.get("base", "password").decode("GBK")
        if cf.has_option("base","dir"):
            g_dir = cf.get("base", "dir", sys.path[0]).decode("GBK")
        if cf.has_option("base","port"):
            g_port = cf.getint("base", "port")
        if cf.has_option("base","anonymous"):
            g_banonymous = cf.getboolean("base", "anonymous")
        if cf.has_option("base","hided"):
            g_hided = cf.getboolean("base" , "hided")
        #////////////////////////////////high level feature
        if cf.has_option("advanced","max_connect"):
            g_max_connect = cf.getint("advanced","max_connect" )
        if cf.has_option("advanced","permission"):
            g_permission = cf.get("advanced","permission","elradfmw").decode("GBK")
        if cf.has_option("advanced","autosetup"):
            g_bautostartup = cf.getboolean("advanced", "autosetup")

        check_ini_para()
        auto_setup(g_bautostartup)
        return  True
    except Exception, ex:
        print ex
        logger.error(ex)
        os.system("pause")
        return False


def check_ini_para():
    global g_user
    global g_password
    global g_dir
    global g_port
    global g_banonymous
    global g_hided
    global g_bautostartup
    global g_max_connect
    global g_permission

    if len(g_permission) == 0:
        g_permission = "elradfmw"
        logger.warning("permission error")
    if g_max_connect < 1:
        g_max_connect =1
        logger.warning("the allowed connecting could not smaller than 1")
    if os.path.exists(g_dir) is False:
        os.makedirs(g_dir)
        logger.info("create dir : " + g_dir)




def run():
    global g_user
    global g_password
    global g_dir
    global g_port
    global g_banonymous
    global g_hided
    global g_bautostartup
    global g_max_connect
    global g_permission

    logger.info("currnt dir : " +g_dir)
    print ("currnt dir : " +g_dir)

    try:
        authorizer = DummyAuthorizer()
        if g_banonymous:
            authorizer.add_anonymous(g_dir,perm=g_permission)
        else:
            authorizer.add_user(g_user, g_password, g_dir, perm=g_permission)
        handler = FTPHandler
        handler.authorizer = authorizer
        server = ThreadedFTPServer(("0.0.0.0", g_port), handler)
        server.max_cons = g_max_connect
        server.serve_forever()


    except Exception,ex:
        print ex
        logger.error(ex)
        os.system("pause")
        return


def hide_wnd():
    if platform.system() != "Windows":
        return
    global  g_hided
    if g_hided is False:
        logger.info("windoes not hided")
        return
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        logger.debug("windows hided")
        # ctypes.windll.kernel32.CloseHandle(whnd)

def auto_setup(t_bsetup):
    if t_bsetup is False:
        return
    # doing something to setup with windows




if __name__ == "__main__":
    if read_config():
        hide_wnd()
        run()



```


# 运行效果图
![image](http://note.youdao.com/yws/api/group/27115823/file/106685060?method=getImage&width=640&height=640&version=1&cstk=dWk145O9)
