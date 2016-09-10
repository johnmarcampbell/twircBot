from datetime import datetime as dt
import re
from src.CommandSuite import CommandSuite

class ConnectivityMonitorSuite(CommandSuite):
    """Suite for monitor health of connection to chat"""

    def __init__(self, name):
        """Init function for ConnectivityMonitorSuite"""
        CommandSuite.__init__(self, name)
        self.config = self.config_manager.parse_file('config/defaultConnectivityManagerSuite.config')
        self.uptime_string = '\\' + self.config['invoke_string'] + self.config['uptime_suffix']
        self.bornTime = dt.utcnow()
        self.last_data = dt.utcnow()

    def parse(self, data):
        """Parse chat data and log it"""
        self.chat_tuple = self.parse_chat(data, self.config['nick'])
        message = self.chat_tuple[1]
        channel = self.chat_tuple[2]
        uptime_match = re.search(self.uptime_string, data)
        self.last_data = dt.utcnow()

        if uptime_match:
            uptime_message = 'Uptime: ' + str(self.lifetime)
            self.host.privmsg(channel, uptime_message)

    def check_timers(self):
        """Function to check timers"""

        now = dt.utcnow()
        inputDelta = now - self.last_data
        self.lifetime = now - self.bornTime

        if inputDelta.seconds > self.config['reconnect_timer']:
            self.host.reconnect = True
            self.last_data = now
        else:
            self.host.reconnect = False

        if self.lifetime.seconds > self.config['stayalive_timer'] and self.config['stayalive_timer'] > 0:
            self.host.stayAlive = False
