#!/usr/bin/python
# -*- coding: UTF-8 -*-
from xyacqbot.Cqserver import Cqserver
from xyacqbot.xyazhServer.ConsoleMessage import ConsoleMessage

ConsoleMessage.DEBUG_LEVEL = 10

cq_server = Cqserver("127.0.0.1", 5700, 5710, 8080)
cq_server.serverRun()