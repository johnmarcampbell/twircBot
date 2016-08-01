import socket
import sys
import re
from datetime import datetime as dt
from .ConfigReader import ConfigReader as cr


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
        reader = cr()
        self.config = reader.parse_file("config/default.config")
        if( config_file_name ):
            self.config = reader.parse_file(config_file_name)

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
        if self.isConnected:
            self.disconnect()

        finishMessage = "TwircBot is going to sleep now..."
        self.logData(finishMessage)
        
        
    def connect(self):
        """ Connect to twitch chat """

        connectMessage = "Attempting to connect... "
        self.logData(connectMessage)

        user_string = 'USER ' + self.config['nick']
        nick_string = 'NICK ' + self.config['nick']
        oauth_string = 'PASS oauth:' + self.config['oauth']
        cap_req_string = 'CAP REQ :twitch.tv/membership'

        self.irc = socket.socket()
        self.irc.settimeout(self.config['connect_timeout'])
        self.irc.connect((self.config['host'], self.config['port']))
        self.last_data = dt.utcnow()

        self.irc.settimeout(self.config['receive_timeout'])
        self.send(user_string) 
        self.send(oauth_string) 
        self.send(nick_string) 
        self.send(cap_req_string) 

        self.isConnected = True;

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
        self.send('PRIVMSG #' + channel + ' :' + message)
    
    def join(self, channel):
        """ Join a channel. """
        self.send('JOIN #' + channel)
    
    def part(self, channel):
        """ Leave a channel. """
        self.send('PART #' + channel)
    
    def processData(self, data):
        """ Break up the datastream into lines and decide what to do with them. """
        for line in data.splitlines():
            words = line.split()
            if words[0] == 'PING':
                self.pong()
                self.logData(line)
                continue

            """ Define some regex search strings """
            privmsg_string = ':(\S+)!\S+@\S+\.tmi\.twitch\.tv PRIVMSG \#(\S+) :(.*)'
            join_string = ':(\S+)!\S+@\S+\.tmi\.twitch\.tv JOIN \#(\S+)'
            part_string = ':(\S+)!\S+@\S+\.tmi\.twitch\.tv PART \#(\S+)'
            mode_string = ':jtv MODE \#(\S+) ([+]|[-])o (\S+)'
            name_list_string = ':' + self.config['nick'] + '\.tmi\.twitch\.tv 353 ' + self.config['nick'] + ' \= \#(\S+) :(.*)'
            name_list_end_string = ':' + self.config['nick'] + '\.tmi\.twitch\.tv 366 ' + self.config['nick'] + ' \#(\S+) :End of \/NAMES list'

            privmsgMatch = re.search(privmsg_string, line)
            if privmsgMatch:
                user = privmsgMatch.group(1)
                channel = privmsgMatch.group(2)
                message = privmsgMatch.group(3)
                log_string = "PRIVMSG #" + channel + " " + user + ": " + message
                self.logData(log_string)
                if re.search('smart', message):
                    self.privmsg(self.config['nick'], 'You are smart!')
                continue 

            joinMatch = re.search(join_string, line)
            if joinMatch:
                user = joinMatch.group(1)
                channel = joinMatch.group(2)
                log_string = "JOIN #" + channel + " " + user 
                self.logData(log_string)
                continue

            partMatch = re.search(part_string, line)
            if partMatch:
                user = partMatch.group(1)
                channel = partMatch.group(2)
                log_string = "PART #" + channel + " " + user 
                self.logData(log_string)
                continue

            modeMatch = re.search(mode_string, line)
            if modeMatch:
                user = modeMatch.group(3)
                channel = modeMatch.group(1)
                plus_or_minus = modeMatch.group(2)
                log_string = "MODE #" + channel + " " + plus_or_minus + "o " + user 
                self.logData(log_string)
                continue

            name_list_match = re.search(name_list_string, line)
            if name_list_match:
                channel = name_list_match.group(1)
                log_string = "NAMES #" + channel + ": "
                for name in name_list_match.group(2).split():
                    log_string += name + " "
                self.logData(log_string)
                continue

            name_list_end_match = re.search(name_list_end_string, line)
            if name_list_end_match:
                channel = name_list_end_match.group(1)
                log_string = "NAMES #" + channel + " End list"
                self.logData(log_string)
                continue

            self.logData(line)


    def logData(self, data):
        """ Timestamps a line of output and send it to the logfile """
        current_time = dt.strftime(dt.utcnow(), self.config['time_format'])
        log_file = open(self.config['log'],"a")
        log_file.write(current_time + " " + data + "\n")
        log_file.close()

    def checkTimers(self):
        """Check the various state timers and determine if we need to take action"""

        # Check reconnect time
        now = dt.utcnow()
        inputDelta = now - self.last_data
        lifetime = now - self.bornTime

        if inputDelta.seconds > self.config['reconnect_timer']:
            log_message = "Reconnect time is up. Time to reconnect!"
            self.logData(log_message)
            self.reconnect = True
        else:
            self.reconnect = False

        if lifetime.seconds > self.config['stayalive_timer'] and self.config['stayalive_timer'] > 0:
            log_message = "StayAlive time is up. Time to go to sleep!"
            self.logData(log_message)
            self.stayAlive = False


        