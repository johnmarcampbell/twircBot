import unittest
import os
from datetime import datetime as dt
from context import *

class testLogger(unittest.TestCase):
    """Test cases for logger"""

    def setUp(self):
        """Set up some important variables"""
        self.maxDiff = None
        self.log_file= 'testLog.log'
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        self.log = Logger('logger')
        self.log.config['log'] = self.log_file
        self.data_type_list = ['privmsg', 'whisper', 'join', 'part', 'mode',
                                'ping', 'names_start', 'names_end', 'cap', 
                                'greet', 'userstate', 'roomstate', 'unknown',
                                'super_unknown']

        # Create a bunch of ServerData's and add them to a ServerBlock
        (channel, user, content) = ('testChannel', 'testUser', 'testContent')
        self.privmsg = ServerData(d_type = 'privmsg',
                            channel = channel, user = user, content = content)
        self.whisper = ServerData(d_type = 'whisper',
                            channel = channel, user = user, content = content)
        self.join = ServerData(d_type = 'join',
                            channel = channel, user = user, content = content)
        self.part = ServerData(d_type = 'part',
                            channel = channel, user = user, content = content)
        self.mode = ServerData(d_type = 'mode',
                            channel = channel, user = user, content = content)
        self.ping = ServerData(d_type = 'ping',
                            channel = channel, user = user, content = content)
        self.names_start = ServerData(d_type = 'names_start',
                            channel = channel, user = user, content = content)
        self.names_end = ServerData(d_type = 'names_end',
                            channel = channel, user = user, content = content)
        self.cap = ServerData(d_type = 'cap',
                            channel = channel, user = user, content = content)
        self.greet = ServerData(d_type = 'greet',
                            channel = channel, user = user, content = content)
        self.userstate = ServerData(d_type = 'userstate',
                            channel = channel, user = user, content = content)
        self.roomstate = ServerData(d_type = 'roomstate',
                            channel = channel, user = user, content = content)
        self.unknown = ServerData(d_type = 'unknown',
                            channel = channel, user = user, content = content)
        self.super_unknown = ServerData('Raw data', d_type = 'super_unknown',
                            channel = channel, user = user, content = content)

        data_list = [self.privmsg, self.whisper, self.join, self.part,
                    self.mode, self.ping, self.names_start, self.names_end,
                    self.cap, self.greet, self.userstate, self.roomstate,
                    self.unknown, self.super_unknown]
        self.block = ServerBlock('', data_list)

        self.privmsg_string = 'PRIVMSG #testChannel testUser: testContent'
        self.whisper_string = 'WHISPER testUser: testContent'
        self.join_string = 'JOIN #testChannel testUser'
        self.part_string = 'PART #testChannel testUser'
        self.mode_string = 'MODE #testChannel testContento testUser'
        self.ping_string = 'PING'
        self.names_start_string = 'NAMES #testChannel: testContent'
        self.names_end_string = 'NAMES #testChannel End list'
        self.cap_string = 'CAP #testContent'
        self.greet_string = 'GREET #testContent'
        self.userstate_string = 'USERSTATE #testContent'
        self.roomstate_string = 'ROOMSTATE #testContent'
        self.unknown_string = 'UNKNOWN #'
        self.super_unknown_string = 'Raw data'


    def test_parse_default(self):
        """
        Test default behavior: only read privmsgs, whispers,
        joins, and parts
        """
        now = dt.strftime(dt.utcnow(), self.log.config['time_format']) + " "
        exemplar_string = now + self.privmsg_string + '\n'
        exemplar_string += now + self.whisper_string + '\n'
        exemplar_string += now + self.join_string + '\n'
        exemplar_string += now + self.part_string + '\n'

        self.log.parse(self.block)

        with open(self.log_file, 'r') as f:
            self.assertEqual(f.read(), exemplar_string)

        os.remove(self.log_file)

    def test_parse_all(self):
        """ Test parse() when reading all data types: """
        now = dt.strftime(dt.utcnow(), self.log.config['time_format']) + " "
        exemplar_string = now + self.privmsg_string + '\n'
        exemplar_string += now + self.whisper_string + '\n'
        exemplar_string += now + self.join_string + '\n'
        exemplar_string += now + self.part_string + '\n'
        exemplar_string += now + self.mode_string + '\n'
        exemplar_string += now + self.ping_string + '\n'
        exemplar_string += now + self.names_start_string + '\n'
        exemplar_string += now + self.names_end_string + '\n'
        exemplar_string += now + self.cap_string + '\n'
        exemplar_string += now + self.greet_string + '\n'
        exemplar_string += now + self.userstate_string + '\n'
        exemplar_string += now + self.roomstate_string + '\n'
        exemplar_string += now + self.unknown_string + '\n'
        exemplar_string += now + self.super_unknown_string + '\n'

        self.log.config['types_to_log'] = self.data_type_list
        self.log.parse(self.block)

        with open(self.log_file, 'r') as f:
            self.assertEqual(f.read(), exemplar_string)

        os.remove(self.log_file)


    def tearDown(self):
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)
        

if __name__ == '__main__':
    unittest.main()
