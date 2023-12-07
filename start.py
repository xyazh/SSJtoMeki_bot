#!/usr/bin/python
# -*- coding: UTF-8 -*-

from cqpy import Cqserver
from cqpy.xyazhServer.ConsoleMessage import ConsoleMessage
from cqpy.I18n.Config import Config as I18nConfig
from cqpy.I18n.I18n import I18n
from cqpy import LoopEvent
ConsoleMessage.DEBUG_LEVEL = 6
I18nConfig.LANG = "cn"
LoopEvent.start()
cq_s = Cqserver("127.0.0.1", 5700, 5710)
cq_s.serverRun()