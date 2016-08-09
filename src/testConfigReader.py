from ConfigReader import ConfigReader as cr
import unittest
import os

class testConfigReader(unittest.TestCase):
    """Test cases for configReader"""

    def setUp(self):
        """Set up some important variables"""
        self.example_config_filename = 'testConfig.config'
        
        # Set some values
        oauth_string = 'xxxxxxxxxxx'
        nick_string = 'justinfan4242'
        channels_string = 'channel1 channel2'
        channels_list = ['channel1', 'channel2']
        log_string = 'default.log'
        time_format_string = "'[%Y-%m-%d %H:%M:%S]'"
        time_format_value = '[%Y-%m-%d %H:%M:%S]'
        host_string = 'irc.twitch.tv'
        port_string = '6667'
        port_int = 6667
        block_size_string = '4096'
        block_size_int = 4096
        reconnect_timer_string = '600'
        reconnect_timer_int = 600
        stayalive_timer_string = '0'
        stayalive_timer_int = 0
        connect_timeout_string = '10'
        connect_timeout_float = 10
        receive_timeout_string = '0.1'
        receive_timeout_float = 0.1

        # Write a config file
        config_file_string = 'oauth: ' + oauth_string + '\n'
        config_file_string += 'nick: ' + nick_string + '\n'
        config_file_string += 'channels: ' + channels_string + '\n'
        config_file_string += 'log: ' + log_string + '\n'
        config_file_string += 'time_format: ' + time_format_string + '\n'
        config_file_string += 'host: ' + host_string + '\n'
        config_file_string += 'port: ' + port_string + '\n'
        config_file_string += 'block_size: ' + block_size_string + '\n'
        config_file_string += 'reconnect_timer: ' + reconnect_timer_string + '\n'
        config_file_string += 'stayalive_timer: ' + stayalive_timer_string + '\n'
        config_file_string += 'connect_timeout: ' + connect_timeout_string + '\n'
        config_file_string += 'receive_timeout: ' + receive_timeout_string + '\n'
         
        config_example = open(self.example_config_filename,'w')
        config_example.write(config_file_string)
        config_example.close()

        self.exemplar_config = {
                        'oauth': oauth_string,
                        'nick': nick_string,
                        'channels': channels_list,
                        'log': log_string,
                        'time_format': time_format_value,
                        'host': host_string,
                        'port': port_int,
                        'block_size': block_size_int,
                        'reconnect_timer': reconnect_timer_int,
                        'stayalive_timer': stayalive_timer_int,
                        'connect_timeout': connect_timeout_float,
                        'receive_timeout': receive_timeout_float
                    }

    def test_parse_file(self):
        """Test parse_file()"""
        reader = cr()
        reader.parse_file(self.example_config_filename)
        self.assertEqual(reader.configuration, self.exemplar_config)

    def test_parse_line(self):
        """Test parse_line()"""
        test_dictionary = { 'a': ['1'], 'b': ['2'], 'c': ['3'] }
        line_without_separator = 'a 1'
        line_with_semicolon = 'b: 2'
        line_with_pipe = 'c| 3'

        reader = cr()
        reader.parse_line(line_without_separator)
        reader.parse_line(line_with_semicolon)
        reader.parse_line(line_with_pipe)
        self.assertEqual(reader.configuration, test_dictionary)

    def tearDown(self):
        """Delete the example config file, etc"""
    
        os.remove(self.example_config_filename)
        
if __name__ == '__main__':
    unittest.main()
