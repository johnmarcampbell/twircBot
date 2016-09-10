import re
from src.ConfigReader import ConfigReader

class CommandSuite(object):
    """Abstract class for command suites"""

    def __init__(self, name):
        """Declare some variables, etc"""
        self.name = name
        self.config = {}
        self.config_manager = ConfigReader()
        print("CommandSuite is starting")

    def start(self):
        """Function that gets called after __init__ but before a connection is established"""
        

    def parse(self, data):
        """Test method for this suite"""

        self.data = data

    def finish(self):
        """Function that gets called as TwircBot is shutting down"""
        print("CommandSuite is finishing")
        
    def set_host(self, host):
        """Set the host bot object"""

        self.host = host

    def parse_chat(self, data, nick):
        """Function to parse chat data"""

        message_type = ''
        user = ''
        channel = ''
        message = ''

        for line in data.splitlines():
            words = line.split()

            # Define some regex search strings
            privmsg_string = ':(\S+)!\S+@\S+\.tmi\.twitch\.tv PRIVMSG \#(\S+) :(.*)'
            join_string = ':(\S+)!\S+@\S+\.tmi\.twitch\.tv JOIN \#(\S+)'
            part_string = ':(\S+)!\S+@\S+\.tmi\.twitch\.tv PART \#(\S+)'
            mode_string = ':jtv MODE \#(\S+) ([+]|[-])o (\S+)'
            ping_string = 'PING :tmi.twitch.tv'
            name_list_string = ':' + nick + '\.tmi\.twitch\.tv 353 ' + nick + ' \= \#(\S+) :(.*)'
            name_list_end_string = ':' + nick + '\.tmi\.twitch\.tv 366 ' + nick + ' \#(\S+) :End of \/NAMES list'

            privmsgMatch = re.search(privmsg_string, line)
            joinMatch = re.search(join_string, line)
            partMatch = re.search(part_string, line)
            modeMatch = re.search(mode_string, line)
            pingMatch = re.search(ping_string, line)
            name_list_match = re.search(name_list_string, line)
            name_list_end_match = re.search(name_list_end_string, line)

            if privmsgMatch:
                user = privmsgMatch.group(1)
                channel = privmsgMatch.group(2)
                message = privmsgMatch.group(3)
                message_type = 'privmsg'
                log_string = "PRIVMSG #" + channel + " " + user + ": " + message

            elif joinMatch:
                user = joinMatch.group(1)
                channel = joinMatch.group(2)
                message_type = 'join'
                log_string = "JOIN #" + channel + " " + user 

            elif partMatch:
                user = partMatch.group(1)
                channel = partMatch.group(2)
                message_type = 'part'
                log_string = "PART #" + channel + " " + user 

            elif modeMatch:
                user = modeMatch.group(3)
                channel = modeMatch.group(1)
                plus_or_minus = modeMatch.group(2)
                message_type = 'mode'
                message = plus_or_minus
                log_string = "MODE #" + channel + " " + plus_or_minus + "o " + user 

            elif pingMatch:
                message_type = 'ping'
                message = data

            elif name_list_match:
                channel = name_list_match.group(1)
                message_type = 'names_start'
                log_string = "NAMES #" + channel + ": "
                message = name_list_match.group(2)
                for name in name_list_match.group(2).split():
                    log_string += name + " "

            elif name_list_end_match:
                channel = name_list_end_match.group(1)
                message_type = 'names_end'
                log_string = "NAMES #" + channel + " End list"

            else:
                channel = ''
                message_type = 'unknown'
                user = ''
                message = data
            

        return [message_type, message, channel, user]

    def check_timers(self):
        """Function for checking timers"""
        
