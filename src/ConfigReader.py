import re

class ConfigReader(object):

    """
    A class that reads a configuration file and generates a dictionary
    of configuration parameters
    """

    def __init__(self):
        """Initialize some variables"""
        self.configs = {}
        

    def parse_file(self, config_file_name, is_default = False):
        """
        This function opens a file containing one or many configurations
        and sends the text to parse_text_block()
        """

        with open(config_file_name, 'r') as f:
            text_block = f.read()
            self.parse_text_block(text_block, is_default)

        self.check_types()
        return self.configs['default']


    def parse_text_block(self, block, is_default):
        """
        This function takes some block of text, and divides it into sections,
        each of which correspond to one configuration spec. It then calls a
        function to parse each section.
        """

        config_name = "default"
        self.configs[config_name] = ''

        for line in block.splitlines():
            if len(line) == 0:
                continue
            if line[0] == '%':
                config_name = line[1:]
                self.configs[config_name] = ''
            else:
                self.configs[config_name] += line + '\r\n'

        for key in self.configs:
            self.configs[key] = self.parse_config_text(self.configs[key])

        if is_default:
            self.check_default_config()


    def parse_config_text(self, text):
        """
        This function takes a block of text that corresponds to only *one*
        config and turns it into a dictionary
        """
        config = {}
        
        for line in text.splitlines():
            self.parse_line(line, config)

        return config


    def parse_line(self, line, config):
        """Function to parse individual lines of a config"""
        words = self.split_line(line)

        # Remove semi-colons, etc., used to separate key/values
        key_string = '([a-zA-z0-9]+)' 
        key = re.search(key_string, words[0]).group(1)

        values = words[1:]
        if len(values) == 1:
            values = values[0]
        config[key] = values
    
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

    def check_types(self):
        """Function to check the types of all parameters"""

        for config in self.configs:
            if config != 'template':
                print(self.configs[config])
                for parameter, init_value in self.configs[config].items():
                    print(parameter + " " + str(init_value))

                    # If value should be a list, convert it
                    if self.configs['template'][parameter] == 'list' and (type(init_value).__name__ != 'list'):
                        final_value = [init_value]

                    elif self.configs['template'][parameter] == 'str':
                        final_value = str(init_value)
                    elif self.configs['template'][parameter] == 'int':
                        final_value = int(init_value)
                    elif self.configs['template'][parameter] == 'float':
                        final_value = float(init_value)
                    elif self.configs['template'][parameter] == 'dict':
                        final_value = dict(init_value)
                    else:
                        final_value = init_value

                    self.configs[config][parameter] = final_value
