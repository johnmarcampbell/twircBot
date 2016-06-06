from TwircBot import TwircBot as tw
import sys

if len(sys.argv) >= 2:
    bot = tw(sys.argv[1])
else:
    bot = tw()

bot.print_config()
bot.connect()
