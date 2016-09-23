#!/usr/bin/env python3

from twircbot.twircbot import TwircBot
from twircbot.diceroller import DiceRoller
from twircbot.connectivitymonitor import ConnectivityMonitor
from twircbot.logger import Logger
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


bot.add_suite(ConnectivityMonitor("connectionMonitor"))
bot.add_suite(DiceRoller("diceRoller"))
bot.add_suite(Logger("logger"))

bot.start()
