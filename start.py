#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from cqpy.Cqserver import Cqserver
from cqpy.xyazhServer.ConsoleMessage import ConsoleMessage
from cqpy.I18n.Config import Config as I18nConfig
from cqpy import LoopEvent

ConsoleMessage.DEBUG_LEVEL = 2
I18nConfig.LANG = "cn"

LoopEvent.start()
cq_server = Cqserver("127.0.0.1", 5700, 5710)
cq_server.serverRun()

time.sleep(1)

while True:
    msg = input(">>")
    cq_server.testMsg(553066134,msg)