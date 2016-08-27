import re
from datetime import datetime as dt
from src.CommandSuite import CommandSuite

class LogSuite(CommandSuite):
    """Suite for logging chat data"""

    def __init__(self, name):
        """Init function for logSuite"""
        CommandSuite.__init__(self, name)

        self.config = {}
        self.config['time_format'] =  '[%Y-%m-%d %H:%M:%S]'
        self.config['log'] = "module.log"
        self.config['nick'] = "justinfan4242"
    
    def parse(self, data):
        """ Break up the datastream into lines and decide what to do with them. """

        for line in data.splitlines():
            words = line.split()

            # Define some regex search strings
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
