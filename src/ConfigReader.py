import re

class ConfigReader(object):

    """
    A class that reads a configuration file and generates a dictionary
    of configuration parameters
    """

    def __init__(self):
        """TODO: to be defined """
        self.configuration = {}

        self.config_template = {
                            'oauth': str,
                            'nick': str,
                            'channels': list,
                            'log': str,
                            'time_format': str,
                            'host': str,
                            'port': int,
                            'block_size': int,
                            'reconnect_timer': int,
                            'stayalive_timer': int,
                            'connect_timeout': float,
                            'receive_timeout': float
                        }

        
    def parse_file(self, config_file_name):
        """
        Function to read the configuration file and turn parameters into 
        a dictionary
        """
        with open(config_file_name, 'r') as f:
            lines = f.read()
            for line in lines.splitlines():
                self.parse_line(line)

        self.clean(self.configuration)
        self.check_keys()
        return self.configuration

    def parse_line(self, line):
        """Function to parse individual lines of a configuration file"""
        words = self.split_line(line)

        # Ignore remove semi-colons, etc., used to separate key/values
        key_string = '([a-zA-z09]+)' 
        key = re.search(key_string, words[0]).group(1)

        values = words[1:]
        self.configuration[key] = values
    
    def clean(self, config):
        """Function to clean a configuration dictionary"""
                
        for key in config:
            value = config[key]

            # All values start out as lists. If they are not lists
            # it means they've already been cleaned.
            if type(value) is list:
                # If we didn't read any parameters, delete the key.
                # We'll check later whether or not all keys are present
                if len(value) == 0:
                    del config[key]
                    return

                # if there's only 1 value, we don't want it to be a list...
                # ... except for 'channels' which should always be a list
                if len(value) == 1 and key != 'channels':
                    value = value[0]

            value = self.config_template[key](value)

            config[key] = value
        
    def split_line(self, line):
        """
        This function takes a string and splits it into words, but 
        keeps strings enclosed in single quotes together
        """
            
        # Split line into words around spaces, unless the spaces are in quotations marks
        words = []
        inside_quotes = False
        temp_word = ''
        for i in line:
            if i == "'" and not inside_quotes:
                inside_quotes = True
            elif i == "'" and inside_quotes:
                inside_quotes = False
                words.append(temp_word)
                temp_word = ''
            elif i == ' ' and not inside_quotes and temp_word != '':
                words.append(temp_word)
                temp_word = ''
            elif i == ' ' and inside_quotes:
                temp_word += i
            elif i != ' ':
                temp_word += i

        if temp_word != '':
            words.append(temp_word)

        return words

    def check_keys(self):
        """This function will check the configuration and make sure all mandatory values are present"""
        # Check that configuration has all necessary keys
        for key in self.config_template:
            try:
                value = self.configuration[key]
            except KeyError:
                error_string = "\nError reading config file!!\n"
                error_string += "Configuration file missing parameter: "
                error_string += key
                error_string += '.\nThis *really* shouldn\'t happen! Check the default config.\n'
                error_string += '\n'
                print(error_string)
                raise

            if type(self.configuration[key]) != self.config_template[key]:
                error_string = '\nError reading config file!!\n'
                error_string += 'Configuration parameter "'
                error_string += key
                error_string += '" shoud be of type '
                error_string += self.config_template[key].__name__
                error_string += '. \n'
                print(error_string)
                raise TypeError(type(self.configuration[key]))

        # Check that configuration doesn't have any extraneous keys
        for key in self.configuration:
            try:
                self.config_template[key]
            except KeyError:
                error_string = "\nError reading config file!!\n"
                error_string += "Configuration file tried to set unknown parameter: "
                error_string += key
                error_string += '\n'
                print(error_string)
                raise
