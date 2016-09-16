import re
from datetime import datetime as dt
from .botmodule import BotModule
from .twitchtools import parse_wrapper

class Logger(BotModule):
    """Module for logging chat data"""

    def __init__(self, name):
        """Init function for Logger"""
        BotModule.__init__(self, name)
        self.config = self.config_manager.parse_file('src/config/defaultLogger.config')

    @parse_wrapper
    def parse(self, data):
        """Parse chat data and log it"""
        if data.type not in self.config['types_to_log']:
            return

        current_time = dt.strftime(dt.utcnow(), self.config['time_format'])
        
        if data.type == 'privmsg':
            log_string = "PRIVMSG #" + data.channel + " " + data.user + ": " + data.content
        elif data.type == 'whisper':
            log_string = "WHISPER " + data.user + ": " + data.content
        elif data.type == 'join':
            log_string = "JOIN #" + data.channel + " " + data.user 
        elif data.type == 'part':
            log_string = "PART #" + data.channel + " " + data.user 
        elif data.type == 'mode':
            log_string = "MODE #" + data.channel + " " + data.content+ "o " + data.user 
        elif data.type == 'ping':
            log_string = 'PING'
        elif data.type == 'names_start':
            log_string = "NAMES #" + data.channel + ": " + data.content
        elif data.type == 'names_end':
            log_string = "NAMES #" + data.channel + " End list"
        elif data.type == 'cap':
            log_string = "CAP #" + data.content
        elif data.type == 'greet':
            log_string = "GREET #" + data.content
        elif data.type == 'userstate':
            log_string = "USERSTATE #" + data.content
        elif data.type == 'roomstate':
            log_string = "ROOMSTATE #" + data.content
        elif data.type == 'unknown':
            log_string = "UNKOWN #" + data.raw
        else:
            log_string = str(data.raw)

        log_file = open(self.config['log'],"a")
        log_file.write(current_time + " " + log_string + "\n")
        log_file.close()
