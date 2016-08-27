#!/usr/bin/env python

from src.TwircBot import TwircBot
import sys

try:
    bot = TwircBot(sys.argv[1])
except IndexError:
    bot = TwircBot()

bot.print_config()
bot.start()
