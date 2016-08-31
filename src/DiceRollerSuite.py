import random
import re
from src.CommandSuite import CommandSuite

class DiceRollerSuite(CommandSuite):
    """Suite for rolling dice"""

    def __init__(self, name):
        """Initialize some variables"""
        CommandSuite.__init__(self, name)
        self.config = self.config_manager.parse_file('config/defaultLogSuite.config')
        random.seed()
        self.invoke_match_string = '\!([0-9]+)d([0-9]+)'
        self.invoke_modified_match_string = '\![0-9]+d[0-9]+([+]|[-])([0-9]+)'
        self.invoke_coin_match = '\!flip'
    
    def parse(self, data):
        """Parse chat data and log it"""
        self.chat_tuple = self.parse_chat(data, self.config['nick'])
        message = self.chat_tuple[1]
        base_match = re.search(self.invoke_match_string, data)
        modifier_match = re.search(self.invoke_modified_match_string, data)
        coin_flip_match = re.search(self.invoke_coin_match, data)
        number_of_dice = 0
        die_size = 0
        plus_or_minus = ''
        modifier = 0

        if base_match:
            number_of_dice = int(base_match.group(1))
            die_size = int(base_match.group(2))

            if modifier_match:
                plus_or_minus = modifier_match.group(1) 
                modifier = int(modifier_match.group(2))

            total = self.roll_dice(number_of_dice, die_size, plus_or_minus, modifier)

            print(str(total))
        if coin_flip_match:
            heads_or_tails = self.flip_coin()

            print(heads_or_tails)

        
    def roll_dice(self, number_of_dice, die_size, plus_or_minus, modifier):
        """Function to roll a dice pool"""

        total = 0

        for i in range(0,number_of_dice):
            total += random.randint(1,die_size)

        if plus_or_minus == '+':
            total += modifier
        elif plus_or_minus == '-':
            total -= modifier

        return total

    def flip_coin(self):
        """Function to flip a coin"""


        if random.randint(0,1):
            heads_or_tails = 'heads'
        else:
            heads_or_tails = 'tails'

        return heads_or_tails
        
