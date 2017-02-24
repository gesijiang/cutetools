# -*- coding: UTF-8 -*-

import sys
from socket import *
from .constants import *


def portscan(args):
    opened_ports = []

    host = args[0]
    start_port = args[1]
    end_port = args[2]

    return SHELL_START
