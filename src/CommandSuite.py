import re
from src.ConfigReader import ConfigReader
from src.twitchtools import ServerData

class CommandSuite(object):
    """Abstract class for command suites"""

    def __init__(self, name):
        """Declare some variables, etc"""
        self.name = name
        self.config = {}
        self.config_manager = ConfigReader()
        self.config = self.config_manager.parse_file('config/defaultCommandSuite.config')

    def parse(self, data):
        """Test method for this suite"""

        self.data = data

    def finish(self):
        """Function that gets called as TwircBot is shutting down"""
        
    def set_host(self, host):
        """Set the host bot object"""

        self.host = host

    def check_timers(self):
        """Function for checking timers"""
        
