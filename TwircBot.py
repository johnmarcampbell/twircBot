import socket
import sys
import re

class TwircBot(object):
    """Basic Bot class that reads in a config file, connects to chat rooms,
    and logs the results.
    """
    def __init__(self, config_file):
        """Parse the configuration file to retrieve the config parameters """
        self.host='irc.twitch.tv'
        self.port=6667
        print('Pretending to start TwircBot.')

    def connect(self):
        """Connect to twitch chat"""
        print('Pretending to connect.') 

    def print_config(self):
        """
        Returns a string that contains all the configuration variables
        for a given TwircBot instance.
        """
        config_string = "*****twircBot config*****\n"
        config_string += "Connecting to " + self.host + ":" + str(self.port)
        print(config_string)
