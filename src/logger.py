import re
from datetime import datetime as dt
from .botmodule import BotModule
from .twitchtools import parse_wrapper

class Logger(BotModule):
    """Module for logging chat data"""

    def __init__(self, name):
        """Init function for Logger"""
        BotModule.__init__(self, name)
        self.config = self.config_manager.parse_file('config/defaultLogger.config')

    @parse_wrapper
    def parse(self, data):
        """Parse chat data and log it"""
        self.chat_tuple = (data.type, data.content, data.channel, data.user)
        self.logData(self.chat_tuple)

    def logData(self, data):
        """ Timestamps a line of output and send it to the logfile """
        current_time = dt.strftime(dt.utcnow(), self.config['time_format'])
        
        [message_type, message, channel, user] = data

        if message_type == 'privmsg':
            log_string = "PRIVMSG #" + channel + " " + user + ": " + message
        elif message_type == 'join':
            log_string = "JOIN #" + channel + " " + user 
        elif message_type == 'part':
            log_string = "PART #" + channel + " " + user 
        elif message_type == 'mode':
            log_string = "MODE #" + channel + " " + message + "o " + user 
        elif message_type == 'ping':
            log_string = message
        elif message_type == 'names_start':
            log_string = "NAMES #" + channel + ": "
            for name in name_list_match.group(2).split():
                log_string += name + " "
        elif message_type == 'names_end':
            log_string = "NAMES #" + channel + " End list"
        elif message_type == 'unknown':
            log_string = "UNKOWN #" + message
        else:
            log_string = str(data)

        log_file = open(self.config['log'],"a")
        for line in log_string.splitlines():
            log_file.write(current_time + " " + line + "\n")

        log_file.close()
