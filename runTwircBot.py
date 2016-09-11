#!/usr/bin/env python3

from src.twircbot import TwircBot
from src.diceroller import DiceRoller
from src.connectivitymonitor import ConnectivityMonitor
from src.logger import Logger
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


bot.add_suite(ConnectivityMonitor("connectionMonitor"))
bot.add_suite(DiceRoller("diceRoller"))
bot.add_suite(Logger("logger"))

bot.start()
