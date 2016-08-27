#!/usr/bin/env python3

from src.TwircBot import TwircBot
from src.CommandModule import CommandModule
from src.logModule import logModule
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


module = CommandModule("test")
logger = logModule("logger")
bot.add_module(module)
bot.add_module(logger)

bot.print_config()
bot.start()
