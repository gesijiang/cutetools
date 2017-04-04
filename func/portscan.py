# -*- coding: UTF-8 -*-

import sys
from socket import *
from .constants import *


def portscan(args):
    opened_ports = []

    host = args[0]
    start_port = int(args[1])
    end_port = int(args[2])

    target_ip = gethostbyname(host)
    print "scanning..."
    for port in range(start_port, end_port+1):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(10)
        # 该方法不会抛出异常，只会给出错误码，如果错误码为0表示成功连上了某个端口
        # 如果返回其他值表示出错了，端口没有打开。
        result = sock.connect_ex((target_ip, port))
        print result
        if result == 0:
            opened_ports.append(port)
            print "port", port, "is opened"
    for i in opened_ports:
        print(i)
    return SHELL_START
