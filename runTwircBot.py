from src.TwircBot import TwircBot
import sys

if len(sys.argv) >= 2:
    bot = TwircBot(sys.argv[1])
else:
    bot = TwircBot()

bot.print_config()
bot.start()
