from datetime import datetime as dt
import re
from .botmodule import BotModule
from .twitchtools import parse_wrapper

class ConnectivityMonitor(BotModule):
    """Module for monitor health of connection to chat"""

    def __init__(self, name):
        """Init function for ConnectivityMonitor"""
        BotModule.__init__(self, name)
        self.config = self.config_manager.parse_file('src/config/defaultConnectivityMonitor.config')
        self.uptime_string = '\\' + self.config['invoke_string'] + self.config['uptime_suffix']
        self.bornTime = dt.utcnow()
        self.last_data = dt.utcnow()

    @parse_wrapper
    def parse(self, data):
        """Parse chat data and log it"""
        self.last_data = dt.utcnow()

        if (data.type == 'privmsg') or (data.type == 'whisper'):
            uptime_match = re.search(self.uptime_string, data.content)

            if uptime_match:
                uptime_message = 'Uptime: ' + str(self.lifetime)
                self.reply(data, uptime_message)

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
