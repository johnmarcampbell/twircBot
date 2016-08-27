#!/usr/bin/env python3

from src.TwircBot import TwircBot
from src.CommandModule import CommandModule
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()


module = CommandModule("test")
bot.add_module(module)

bot.print_config()
bot.start()
