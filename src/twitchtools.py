import re
from src.ConfigReader import ConfigReader

class ServerBlock(object):
    """Object that represents a processed block of data from the Twitch IRC server"""

    def __init__(self, raw_data, message_list):
        """Set some initial variables"""
        self.raw_data = raw_data
        self.message_list = message_list
    
class ServerData(object):
    """Object to represent a message from Twitch IRC servers"""

    def __init__(self, raw = '', **kwargs):
        """Instantiate some variables"""
        self.raw = raw
        self.type = ''
        self.channel = ''
        self.user = ''
        self.content = ''

        # message_types = ['UNKOWN', 'PRIVMSG', 'PING', 'WHISPER', 'JOIN', 'PART', 

        for key, value in kwargs.items():
            if key == 'd_type':
                self.type = value
            if key == 'channel':
                self.channel = value
            if key == 'user':
                self.user = value
            if key == 'content':
                self.content = value
    
class DataParser(object):
    """Class for parsing data from Twitch IRC servers"""

    def __init__(self, nick):
        """Docstring"""
    
        self.config = {}
        self.config_manager = ConfigReader()
        self.config = self.config_manager.parse_file('config/twitchtools.config')
        self.nick = nick
        self.config['name_list_string'] = ':' + nick + self.config['name_list_prefix'] + nick + self.config['name_list_prefix']
        self.config['name_list_end_string'] = ':' + nick + self.config['name_list_end_prefix'] + nick + self.config['name_list_end_prefix']
        self.config['whisper_string'] = self.config['whisper_prefix'] + nick + ' :(.*)'

    def parse(self, data):
        """Function to parse server data"""

        data_list = []
        data_type = ''
        channel = ''
        user = ''
        content = ''
        

        for line in data.splitlines():

            privmsgMatch = re.search(self.config['privmsg_string'], line)
            whisperMatch = re.search(self.config['whisper_string'], line)
            joinMatch = re.search(self.config['join_string'], line)
            partMatch = re.search(self.config['part_string'], line)
            modeMatch = re.search(self.config['mode_string'], line)
            pingMatch = re.search(self.config['ping_string'], line)
            name_list_match = re.search(self.config['name_list_string'], line)
            name_list_end_match = re.search(self.config['name_list_end_string'], line)

            if privmsgMatch:
                user = privmsgMatch.group(1)
                channel = privmsgMatch.group(2)
                content = privmsgMatch.group(3)
                data_type = 'privmsg'

            elif whisperMatch:
                user = whisperMatch.group(1)
                content = whisperMatch.group(2)
                data_type = 'whisper'

            elif joinMatch:
                user = joinMatch.group(1)
                channel = joinMatch.group(2)
                data_type = 'join'

            elif partMatch:
                user = partMatch.group(1)
                channel = partMatch.group(2)
                data_type = 'part'

            elif modeMatch:
                user = modeMatch.group(3)
                channel = modeMatch.group(1)
                plus_or_minus = modeMatch.group(2)
                message_type = 'mode'
                content = plus_or_minus

            elif pingMatch:
                data_type = 'ping'

            elif name_list_match:
                channel = name_list_match.group(1)
                data_type = 'names_start'
                content = name_list_match.group(2)

            elif name_list_end_match:
                channel = name_list_end_match.group(1)
                data_type = 'names_end'

            else:
                data_type = 'unknown'
                content = line

            data_list.append(ServerData(line, d_type = data_type, channel = channel, user = user, content = content))

        return ServerBlock(data, data_list)

def parse_wrapper(f):
    """A generic wrapper that splits up different lines of chat"""
    def wrapper(self, server_block):

        for data in server_block.message_list:
            f(self, data)

    return wrapper
