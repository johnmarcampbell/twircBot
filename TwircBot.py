class TwircBot(object):
    """
    Basic Bot class that reads in a config file, connects to chat rooms,
    and logs the results.
    """


    def __init__(self, config_file_name):
        """Parse the configuration file to retrieve the config parameters """
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

        config_file.close()


    def connect(self):
        """Connect to twitch chat"""
        print('Pretending to connect.') 


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

        config_string += "\n***** TwircBot config *****\n"

        print(config_string)
