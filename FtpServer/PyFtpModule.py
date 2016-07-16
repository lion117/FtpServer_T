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


g_user =u"ITC"
g_password =u"ITC123"
g_dir =u"c:"
g_port =2121
g_banonymous = False
g_hided = False

# advanced feature
g_banner =u"welcome to ITC smart_edu ftp for test"
g_listen_ip = u"0.0.0.0"
g_max_connect=256
g_permission = "elradfmw"                #允许权限
g_bserver = 0                    #是否注册为系统服务



def read_config():
    global g_user
    global g_password
    global g_dir
    global g_port
    global g_banonymous
    global g_banner
    global g_listen_ip
    global g_max_connect
    global g_permission
    global g_bserver
    global g_hided
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(os.path.join(os.getcwd(), "FtpConfig.ini"))
        g_user = cf.get("base", "user").decode("GBK")
        g_password = cf.get("base", "password").decode("GBK")
        g_dir = cf.get("base", "dir", sys.path[0]).decode("GBK")
        g_port = cf.getint("base", "port")
        g_banonymous = cf.getboolean("base", "anonymous")
        g_hided = cf.getboolean("base" , "hided")
        return True

        # read advanced feature
        # g_listen_ip = cf.get("advanced","listen_ip" ,"0.0.0.0")
        # g_max_connect = cf.get("advanced","max_connect" ,256)
        # g_permission = cf.get("advanced","permission","elradfmw")
        # g_bserver = cf.get("advanced","bserver",0)
        #
    except Exception, ex:
        print ex
        logger.error(ex)
        os.system("pause")
        return False





def run():
    global g_user
    global g_password
    global g_dir
    global g_port
    global g_banonymous
    global g_banner
    global g_listen_ip
    global g_max_connect
    global g_permission
    global g_bserver
    try:
        authorizer = DummyAuthorizer()
        if g_banonymous:
            authorizer.add_anonymous(g_dir,perm=g_permission)
        else:
            authorizer.add_user(g_user, g_password, g_dir, perm=g_permission)
        handler = FTPHandler
        handler.authorizer = authorizer
        handler.banner = g_banner
        server = ThreadedFTPServer((g_listen_ip, g_port), handler)
        server.max_cons = g_max_connect
        server.serve_forever()


    except Exception,ex:
        print ex
        logger.error(ex)
        os.system("pause")
        return


def hide_wnd():
    global  g_hided
    if g_hided is False:
        logger.info("windoes not hided")
        return

    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        logger.debug("windows hided")
        # ctypes.windll.kernel32.CloseHandle(whnd)



if __name__ == "__main__":
    hide_wnd()
    if read_config():
        run()





