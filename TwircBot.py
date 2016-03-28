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

    def processLine(self, line):
        words = line.split()
        if words[0] == bytes('PING','utf-8'):
            self.irc.send(bytes('PONG :tmi.twitch.tv\r\n', 'utf-8'))
            print('I have received a ping!!')
            self.irc.send(bytes('PRIVMSG #' + self.nick + ' :I received a PING!!\r\n', 'utf-8'));
        for word in words:
            if word == bytes('smart','utf-8'):
                self.irc.send(bytes('PRIVMSG #' + self.nick + ' :You are smart\r\n', 'utf-8'));


    def connect(self):
        """Connect to twitch chat"""
        user_string = bytes('USER ' + self.nick + ' \r\n', 'utf-8')
        nick_string = bytes('NICK ' + self.nick + ' \r\n', 'utf-8')
        oauth_string = bytes('PASS oauth:' + self.oauth + ' \r\n', 'utf-8')
        cap_req_string = bytes('CAP REQ :twitch.tv/membership \r\n', 'utf-8')

        self.irc.connect((self.host, self.port))
        self.irc.send(user_string) 
        self.irc.send(oauth_string) 
        self.irc.send(nick_string) 
        self.irc.send(cap_req_string) 

        for channels in self.channel_list:
            channel_string = bytes('JOIN #' + channels + ' \r\n', 'utf-8')
            self.irc.send(channel_string) 

        while True: 
            data = self.irc.recv(4096)
            if data:
                print(data.decode('utf-8'))
                log_file = open(self.log_file_name,"a")
                log_file.write(data.decode('utf-8'))
                log_file.close()
                self.processLine(data)


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

