import re
from .configreader import ConfigReader
from .twitchtools import ServerData

class BotModule(object):
    """Abstract class for modules"""

    def __init__(self, name):
        """Declare some variables, etc"""
        self.name = name
        self.config = {}
        self.config_manager = ConfigReader()
        self.config = self.config_manager.parse_file('twircbot/config/defaultBotModule.config')

    def parse(self, data):
        """Test method for this module"""

        self.data = data

    def reply(self, in_message, out_message):
        """Send an @-reply to a PRIVMSG or a whisper reply to a WHISPER"""
        if in_message.type == 'privmsg':
            reply_string = '@' + in_message.user + ' ' + out_message
            self.host.privmsg(in_message.channel, reply_string)
        elif in_message.type == 'whisper':
            self.host.whisper(in_message.user, out_message)

    def finish(self):
        """Function that gets called as TwircBot is shutting down"""
        
    def set_host(self, host):
        """Set the host bot object"""

        self.host = host

    def check_timers(self):
        """Function for checking timers"""
        
