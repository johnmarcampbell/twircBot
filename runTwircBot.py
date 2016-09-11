#!/usr/bin/env python3

from src.TwircBot import TwircBot
from src.DiceRollerSuite import DiceRollerSuite
from src.ConnectivityMonitorSuite import ConnectivityMonitorSuite
from src.LogSuite import LogSuite
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


# bot.add_suite(ConnectivityMonitorSuite("connectionMonitor"))
bot.add_suite(DiceRollerSuite("diceRoller"))
bot.add_suite(LogSuite("logger"))

bot.start()
