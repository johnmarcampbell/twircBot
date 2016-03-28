import socket
import sys


class TwircBot(object):
    """
    Basic Bot class that reads in a config file, connects to chat rooms,
    and logs the results.
    """


    def __init__(self, config_file_name):
        """Parse the configuration file to retrieve the config parameters """
        self.irc = socket.socket()
        self.host='irc.twitch.tv'
        self.port=6667
        config_file = open(config_file_name,"r")

        for line in config_file:
            words = line.split()
            if words[0] == "oauth:": 
                self.oauth = line.split()[1]
            elif words[0] == "nick:": 
                self.nick = line.split()[1]
            elif words[0] == "channels:": 
                self.channel_list = line.split()[1:]
            elif words[0] == "log:": 
                self.log_file_name = line.split()[1]

        config_file.close()

    def connect(self):
        """Connect to twitch chat"""
        user_string = 'USER ' + self.nick
        nick_string = 'NICK ' + self.nick
        oauth_string = 'PASS oauth:' + self.oauth
        cap_req_string = 'CAP REQ :twitch.tv/membership'

        self.irc.connect((self.host, self.port))
        self.send(user_string) 
        self.send(oauth_string) 
        self.send(nick_string) 
        self.send(cap_req_string) 

        for channels in self.channel_list:
            channel_string = 'JOIN #' + channels
            self.send(channel_string) 

        while True: 
            data = self.receive()
            if data:
                print(data)
                log_file = open(self.log_file_name,"a")
                log_file.write(data)
                log_file.close()
                self.processData(data)


    def print_config(self):
        """
        Prints a string that contains all the configuration variables
        for a given TwircBot instance.
        """
        config_string = "\n***** TwircBot config *****\n"

        config_string += "Connecting to " + self.nick + "@"
        config_string += self.host + ":" + str(self.port) + "\n"

        config_string += "Channels: "
        for channels in self.channel_list:
            config_string += str(channels) + ", "
        config_string = config_string[:-2] #Remove last comma and space

        config_string += "\nLog file: " + self.log_file_name

        config_string += "\n***** TwircBot config *****\n"

        print(config_string)


    def send(self, message_string):
        """Accept a string, convert it to bytes, and send it."""
        message_bytes = bytes(message_string + '\r\n', 'utf-8')
        self.irc.send(message_bytes)

    
    def receive(self):
        """Accept some bytes from the socket and return them as a string."""
        message_bytes = self.irc.recv(4096)
        message_string = message_bytes.decode('utf-8')
        return message_string

    def pong(self):
        """Send a PONG."""
        self.send('PONG :tmi.twitch.tv\r\n')

    def privmsg(self, channel, message):
        """ Send a private message to a particular channel. """
        self.send('PRIVMSG #' + channel + ' :' + message)
    
    def processData(self, data):
        """ Break up the datastream into lines and decide what to do with them. """
        for lines in data.splitlines():
            words = lines.split()
            if words[0] == 'PING':
                self.pong()
            if 'smart' in words:
                self.privmsg(self.nick, 'You are smart!')

  
