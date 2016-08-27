#!/usr/bin/env python3

from src.TwircBot import TwircBot
from src.CommandSuite import CommandSuite
from src.LogSuite import LogSuite
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


module = CommandSuite("test")
logger = LogSuite("logger")
bot.add_module(module)
bot.add_module(logger)

bot.print_config()
bot.start()
