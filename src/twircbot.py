import socket
import sys
import re
from datetime import datetime as dt
from .configreader import ConfigReader as cr
from .twitchtools import DataParser as dp


class TwircBot(object):
    """
    Basic Bot class that reads in a config file, connects to chat rooms,
    and logs the results.
    """


    def __init__(self, config_file_name = ''):
        """ Parse the configuration file to retrieve the config parameters """
        self.stayAlive = True
        self.isConnected = False
        self.bornTime = dt.utcnow()
        self.suite_list = []
        reader = cr()
        self.config = reader.parse_file("config/default.config")
        if( config_file_name ):
            self.config = reader.parse_file(config_file_name)

        self.parser = dp(self.config['nick'])

    def start(self):
        """Connect to twitch chat and start listening"""
        self.connect()

        temp_data = ''
        while self.stayAlive: 
            self.checkTimers()

            if self.reconnect:
                self.disconnect()
                self.connect()

            data = self.receive()
            if data and (data[-2:] != '\r\n'): # Checks to make sure we got an entire line
                temp_data += data
            elif data:
                data = temp_data + data
                self.processData(data)
                temp_data = ''
                self.last_data = dt.utcnow()

        self.finish()

    def finish(self):
        """Make sure we are disconnect and close log files and everything"""
        self.stayAlive = False
        if self.isConnected:
            self.disconnect()

        for suite in self.suite_list:
            suite.finish()
        finishMessage = "TwircBot is going to sleep now..."
        self.logData(finishMessage)
        
        
    def connect(self):
        """ Connect to twitch chat """

        connectMessage = "Attempting to connect... "
        self.logData(connectMessage)

        user_string = 'USER ' + self.config['nick']
        nick_string = 'NICK ' + self.config['nick']
        oauth_string = 'PASS oauth:' + self.config['oauth']
        member_string = 'CAP REQ :twitch.tv/membership'
        command_string = 'CAP REQ :twitch.tv/commands'

        self.irc = socket.socket()
        self.irc.settimeout(self.config['connect_timeout'])
        self.irc.connect((self.config['host'], self.config['port']))
        self.last_data = dt.utcnow()

        self.irc.settimeout(self.config['receive_timeout'])
        self.send(user_string) 
        self.send(oauth_string) 
        self.send(nick_string) 
        self.send(member_string) 
        self.send(command_string) 

        self.isConnected = True
        self.reconnect = False

        for channel in self.config['channels']:
            self.join(channel)

    def disconnect(self):
        """Disconnect from twitch chat"""
        
        disconnectMessage = "Disconnecting... "
        self.logData(disconnectMessage)

        for channel in self.config['channels']:
            self.part(channel)

        # self.irc.shutdown(socket.SHUT_RDWR)
        self.irc.close()

        self.isConnected = False;

    def print_config(self):
        """
        Prints a string that contains all the configuration variables
        for a given TwircBot instance.
        """
        config_string = "\n***** TwircBot config *****\n"

        config_string += "Connecting to " + self.config['nick'] + "@"
        config_string += self.config['host'] + ":" + str(self.config['port']) + "\n"

        config_string += "Channels: "
        for channels in self.config['channels']:
            config_string += str(channels) + ", "
        config_string = config_string[:-2] #Remove last comma and space

        config_string += "\nLog file: " + self.config['log']
        config_string += "\nTime format: " + self.config['time_format']
        config_string += "\nReconnect timer: " + str(self.config['reconnect_timer'])
        config_string += "\nStayAlive timer: " + str(self.config['stayalive_timer'])

        config_string += "\n***** TwircBot config *****\n"

        print(config_string)


    def send(self, message_string):
        """ Accept a string, convert it to bytes, and send it. """
        message_bytes = bytes(message_string + '\r\n', 'utf-8')
        self.irc.send(message_bytes)
    
    def receive(self):
        """ Accept some bytes from the socket and return them as a string. """
        try:
            message_bytes = self.irc.recv(self.config['block_size'])
            message_string = message_bytes.decode('utf-8')
        except BlockingIOError:
            message_string = ''
        except socket.timeout:
            message_string = ''

        return message_string

    def pong(self):
        """ Send a PONG. """
        self.send('PONG :tmi.twitch.tv\r\n')

    def privmsg(self, channel, message):
        """ Send a private message to a particular channel. """
        message_text = 'PRIVMSG #' + channel + ' :' + message
        log_text = 'PRIVMSG #' + channel + ' ' + self.config['nick'] + ' (self): ' + message
        self.send(message_text)
        self.logData(log_text)

    def whisper(self, user, message):
        """Send a whisper to a user"""
        whisper_string = '/w ' + user + ' ' + message
        self.privmsg('jtv', whisper_string)
    
    def join(self, channel):
        """ Join a channel. """
        self.send('JOIN #' + channel)
    
    def part(self, channel):
        """ Leave a channel. """
        self.send('PART #' + channel)
    
    def processData(self, raw_data):
        """ Break up the datastream into lines and decide what to do with them. """
        server_block = self.parser.parse(raw_data)

        for suite in self.suite_list:
            suite.parse(server_block)

        for data in server_block.message_list:
            if data.type == 'ping':
                self.pong()
                self.logData('PONG')

    def logData(self, data):
        """ Timestamps a line of output and send it to the logfile """
        current_time = dt.strftime(dt.utcnow(), self.config['time_format'])
        log_file = open(self.config['log'],"a")
        log_file.write(current_time + " " + data + "\n")
        log_file.close()

    def checkTimers(self):
        """Check the various state timers and determine if we need to take action"""

        for suite in self.suite_list:
            suite.check_timers()

    def add_suite(self, suite):
        """Add a command suite to TwircBot's suite list"""

        self.suite_list.append(suite)
        suite.set_host(self)
        suite_type = type(suite).__name__
        message = "Adding suite (name - type): " + suite.name + " - " + suite_type
        self.logData(message)
