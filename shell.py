# -*- coding: UTF-8 -*-

import os
import sys
import socket
import getpass
import platform
import signal
import shlex
import subprocess
from func import *

bind_map = {}


'''使命令与处理函数建立对应关系'''


def bind_command(name, func):
    bind_map[name] = func


'''建立映射'''


def init():
    # 退出shell
    bind_command("exits", exits)


'''shell循环接受命令'''


def loop():
    status = SHELL_START
    while status == SHELL_START:
        # 打印提示符
        display()
        ignore_signal()

        try:
            # 读命令
            cmd = sys.stdin.readline()

            # 解析命令,返回一个列表
            cmd_list = cmd_split(cmd)

            # 将命令中的环境变量使用真实值进行替换
            cmd_list = cmd_pre(cmd_list)

            # 执行命令，并返回状态
            status = cmd_execute(cmd_list)

        except:
            # sys.exc_info 函数返回一个包含三个值的元组(type, value, traceback)
            _, err, _ = sys.exc_info()
            print(err)


'''打印提示'''


def display():
    # 主机名
    hostname = socket.gethostname()

    # 用户名
    username = getpass.getuser()

    # 路径
    cwd = os.getcwd()
    basedir = os.path.basename(cwd)
    # 用户根目录
    if cwd == os.path.expanduser('~'):
        basedir = '~'

    # 输出
    sys.stdout.write("[%s@%s %s]$ " % (username, hostname, basedir))
    sys.stdout.flush()


'''忽略中断'''


def ignore_signal():
    if platform.system() != "Windows":
        # 忽略 Ctrl-Z
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    # 忽略 Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_IGN)


'''按空格划分'''


def cmd_split(string):
    return shlex.split(string)


'''替换环境变量'''


def cmd_pre(old_list):
    new_list = []
    for cmd in old_list:
        '''
        if cmd[0] == '$':
            new_list.append(os.getenv(cmd[1:]))
        else:
        '''
        new_list.append(cmd)
    return new_list


'''执行'''


def cmd_execute(meta_cmd):

    if meta_cmd:
        cmdname = meta_cmd[0]
        cmdargs = meta_cmd[1:]

    # 调用相应函数
    if cmdname in bind_map:
        return bind_map[cmdname](cmdargs);

    # 监听 Ctrl-C 信号
    signal.signal(signal.SIGINT, handler_kill)

    # 创建子进程
    if platform.system() != "Windows":
        # Unix 平台
        # 调用子进程执行命令
        p = subprocess.Popen(meta_cmd)

        # 父进程从子进程读取数据，直到读取到 EOF
        p.communicate()
    else:
        command = ""
        command = ' '.join(meta_cmd)
        os.system(command)

    # 返回状态
    return SHELL_START


def handler_kill(signum, frame):
    raise OSError("Killed!")


def main():
    init()
    loop()


if __name__ == "__main__":
    main()
