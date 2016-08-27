#!/usr/bin/env python3

from src.TwircBot import TwircBot
from src.CommandSuite import CommandSuite
from src.LogSuite import LogSuite
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


bot.add_suite(CommandSuite("test"))
bot.add_suite(LogSuite("logger"))

bot.print_config()
bot.start()
