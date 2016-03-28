from TwircBot import TwircBot as tw
import sys

bot = tw(sys.argv[1])
bot.print_config()
bot.connect()
